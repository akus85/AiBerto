from transformers import AutoTokenizer                                                                                                                     
                                                                                                                                                             
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B")                                                                                                     
                                                                                                                                                             
system_it = (                                                                                                                                              
    "Sei un assistente che aiuta a riscrivere email professionali "                                                                                        
    "in tono cordiale ma diretto. Quando ricevi un testo, restituisci "                                                                                    
    "tre varianti con livelli di formalità diversi."                                                                                                       
)                                                                                                                                                          
                                                                                                                                                             
system_en = (                                                                                                                                              
    "You are an assistant that helps rewrite professional emails "                                                                                         
    "in a cordial but direct tone. When you receive a text, return "
    "three variants with different levels of formality."
)                                                                                                                                                          
   
print(f"Italiano: {len(tok.encode(system_it))} token")                                                                                                     
print(f"English:  {len(tok.encode(system_en))} token")