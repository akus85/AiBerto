import dspy
from dspy.retrievers import Embeddings

lm = dspy.LM("ollama_chat/llama3.2", api_base="http://localhost:11434")
embedder = dspy.Embedder("ollama/nomic-embed-text", api_base="http://localhost:11434")
dspy.configure(lm=lm)

corpus = [
    "Parigi è la capitale e la città più grande della Francia.",
    "William Shakespeare scrisse Romeo e Giulietta alla fine del XVI secolo.",
    "Marte è conosciuto come il Pianeta Rosso a causa dell'ossido di ferro sulla sua superficie.",
    "L'Oceano Pacifico è il più grande e profondo oceano della Terra.",
    "Leonardo da Vinci dipinse la Gioconda all'inizio del XVI secolo.",
    "L'aurora boreale è causata da particelle cariche provenienti dal Sole che interagiscono con il campo magnetico terrestre.",
    "L'acqua bolle a 100 gradi Celsius al livello del mare.",
    "La Grande Muraglia cinese fu costruita nel corso di molti secoli per proteggere dalle invasioni.",
]

retriever = Embeddings(embedder=embedder, corpus=corpus, k=3)

trainset = [
    dspy.Example(question="Qual è la capitale della Francia?", answer="Parigi").with_inputs("question"),
    dspy.Example(question="Chi scrisse Romeo e Giulietta?", answer="Shakespeare").with_inputs("question"),
    dspy.Example(question="Quale pianeta è noto come il Pianeta Rosso?", answer="Marte").with_inputs("question"),
    dspy.Example(question="Qual è l'oceano più grande?", answer="Pacifico").with_inputs("question"),
    dspy.Example(question="Chi dipinse la Gioconda?", answer="Leonardo da Vinci").with_inputs("question"),
]

class RAG(dspy.Module):
    def __init__(self):
        self.retrieve = retriever
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question)
        return self.generate(context=context, question=question)

def answer_match(example, pred, trace=None):
    return example.answer.lower() in pred.answer.lower()

optimizer = dspy.BootstrapFewShot(metric=answer_match, max_bootstrapped_demos=4)
optimized_rag = optimizer.compile(RAG(), trainset=trainset)

result = optimized_rag(question="Cosa causa l'aurora boreale?")
print(result.answer)
