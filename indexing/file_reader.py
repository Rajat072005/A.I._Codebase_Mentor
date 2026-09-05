

import os
import time
from indexing import llm_metadata_generator, metadata_cache, build_document , batch_indexer

SKIP_FOLDERS = {".git", "node_modules", "__pycache__", "venv", "dist", "build"}

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".css", ".html", ".json", ".md", ".txt"
}

IGNORE_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    ".config.js", "robot.json"
}

                                 
         
                                                               

                              
                                              
                                                      
                                             

           
                                                        

              
                                                
         
                    

                                                  
                                            
                                                              

                            
                                                   

                                      
                          
                                                     
                          

                                                  

                  
                                                                   
                                        

                                                                         
                                                                                   
                                  
                              
                                        
                                                 
                                         
                                        
                       

                                                                                    
                                    
                                        
                                                               
                                         
                    

                                        
                                                                        

                                                  
    
                      

def read_repository(repo_path):

    raw_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS]

        for file in files:
            extension = os.path.splitext(file)[1]

            if file in IGNORE_FILES:
                continue
            if extension not in ALLOWED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                raw_files.append({"path": file_path, "content": content})
            except Exception as error:
                print(f"  [skip] Could not read {file_path}: {error}")

    print(f"Total files read: {len(raw_files)}")

                                                                           
                                                                          
    repo_name = os.path.basename(os.path.dirname(repo_path.rstrip("/\\")))

    metadata_by_path = batch_indexer.get_metadata_for_repo(raw_files, repo_path, repo_name)

    all_files = []
    for f in raw_files:
        meta = metadata_by_path.get(f["path"]) 
        knowledge_document = build_document.build_knowledge_document(meta)
        all_files.append({
            "path": f["path"],
            "knowledge_document": knowledge_document,
            "content": f["content"],
        })

    return all_files
