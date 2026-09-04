
import llm_explainer
import question_classifier
import storage
import utils
import os
import repository_manager
import memory
import context_builder
import query_router
import retrieval_filter
import prompt_builder
import repo_retrieval_files
import confidence_handler
import strategy_executor
choice = input(
    f"""
1. Index Repository
2. Ask Questions

Enter Your Choice : """
)


if(choice == "1"):
    # repo_url = "https://github.com/Rajat072005/SyncSphere-Website"
    repo_url_input = input(
        "Provide the repository url : "
    )
    repo_name = utils.extract_repo_name(repo_url_input)
    repo_folder = utils.create_repo_folder(repo_name)
    if os.path.exists(repo_folder):
        user_index_input = input(
            "Repository already exists. Re-index? (y/n) : "
        )
        if user_index_input.lower() == 'y':
            repository_manager.reindex_repository(repo_url_input)
        elif user_index_input.lower() == 'n':
            exit()
    else:
        repository_manager.reindex_repository(repo_url_input)

    

elif(choice == "2"):
    repos = utils.get_saved_repo()
    utils.display_repositories(repos)
    user_choice = int(input(
        f"""
Select Repository : """
    ))
    if user_choice < 1 or user_choice > len(repos):
        print("Invalid Repository Selection")
        exit()
    else : 
        
        print(f"\nSelected Repository : {repos[user_choice-1]}")
        selected_repo = repos[user_choice-1]
        repo_folder = f"data/{selected_repo}"
        repo_code_folder = f"{repo_folder}/repository"
        repo_info = storage.load_json(f"{repo_folder}/repo_info.json")
        last_commit_hash = repo_info['last_commit_hash']
        remote_commit_hash = utils.get_remote_commit_hash(repo_info['repo_url'])
        if remote_commit_hash is None:
            print("Could not check remote repository.")
        elif last_commit_hash != remote_commit_hash:
            print("executing...")
            repository_manager.reindex_repository(repo_info['repo_url'])
        chunks = storage.load_json(f"{repo_folder}/chunks.json")
        embeddings = storage.load_json(f"{repo_folder}/embeddings.json")
        chunk_map = utils.build_chunkmap(chunks)
        embedding_map = utils.build_embeddingmap(embeddings)
        while True:
            question = input(
                "Ask a question about the repository: "
            )
            if question.lower() == "exit":
                print("Goodbye")
                break
            question_type = question_classifier.question_classifier(question)
            print("question type : " , question_type)
            current_memory = memory.get_memory(repo_folder)
            followup_words = [
                "this",
                "that",
                "here",
                "there",
                "it",
                "this function",
                "that function"
            ]
            isFollowup = False
            if question_type != "casual":
                question_words = question.lower().split()
                for word in followup_words:
                    if word in question_words:
                        if current_memory["last_files"]:
                            isFollowup = True
                            break

        
            if question_type == "casual":
                prompt = prompt_builder.build_prompt(intent , question , "")
                answer = llm_explainer.generate_answer(prompt)
                print(answer)
                continue
            else :
                strategy = STRATEGIES[question_type]
                context_chunks , top_score = strategy_executor.execute_strategy(question , strategy , chunks , chunk_map , embeddings)

                if confidence_handler._should_answer(top_score):
                    context = context_builder.build_context(chunk_map , context_chunks)
                    prompt = prompt_builder.build_prompt(intent , question , context)
                    # answer
                    # print(answer) 
                else:
                    answer = confidence_handler.build_low_confidence_message(question)
                    print(answer)

            # for index, result in enumerate(semantic_results, start=1):
            #         print(f"Retrieved File from semantic results {index}: {result['path']}")
            
            # for index, result in enumerate(keyword_results, start=1):
            #         print(f"Retrieved File from keyword results  {index}: {result['path']}")

            # for index, result in enumerate(merged_results, start=1):
            #         print(f"Retrieved File from merged results with rrf {index}: {result['path']}",
            #               f"rrf score of result {index} : {result['rrf_score']}")
            # for index, result in enumerate(reranked_results, start=1):
            #         print(f"Retrieved File from reranked results {index}: {result['path']}")

            
            
            # memory.update_memory(repo_folder , question , question_type , reranked_results , answer)

