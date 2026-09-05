               

                       
              
               
                
             
               
                
                  
                      
               
                
                   
            
                 
              
                         
                      
                           
                      
                        

   
OBJECT = [
    "project",
    "repository",
    "application",
    "system",
    "codebase",
    "software",
    "platform",
]
BUSINESS_FEATURES = [
    "login",
    "signup",
    "authentication",
    "authorization",
    "payment",
    "orders",
    "cart",
    "dashboard",
    "profile",
    "notification",
    "search",
]

TECHNICAL_FEATURES = [
    "routing",
    "middleware",
    "API",
    "database",
    "cache",
    "state management",
    "configuration",
    "request handling",
    "session management",
    "validation",
]

FEATURES = BUSINESS_FEATURES + TECHNICAL_FEATURES

INTENT_BLUEPRINT = {
                                
              
                                
    "overview": [
        {
            "pattern": "What does this {object} do?",
            "variables": {
                "object": [
                    "project",
                    "repository",
                    "application",
                    "system",
                    "codebase",
                    "software",
                    "platform",
                ]
            },
            "category": "purpose",
        },
        {
            "pattern": "Give me an overview of this {object}.",
            "variables": {"object": OBJECT},
            "category": "Overview",
        },
        {
            "pattern": "Explain this {object}.",
            "variables": {"object": OBJECT},
            "category": "explanation",
        },
        {
            "pattern": "Summarize this {object}.",
            "variables": {"object": OBJECT},
            "category": "summary",
        },
        {
            "pattern": "What problem does this {object} solve?",
            "variables": {"object": OBJECT},
            "category": "problem",
        },
        {
            "pattern": "Introduce this {object}?",
            "variables": {"object": OBJECT},
            "category": "introduction",
        },
        {
            "pattern": "What is the purpose of this {object}?",
            "variables": {"object": OBJECT},
            "category": "goal",
        },
        {
            "pattern": "Describe this {object}.",
            "variables": {"object": OBJECT},
            "category": "description",
        },
        {
            "pattern": "Explain this {object} at a high level.",
            "variables": {"object": OBJECT},
            "category": "high_level",
        },
        {
            "pattern": "Help me understand this {object}.",
            "variables": {"object": OBJECT},
            "category": "learning",
        },
        {
            "pattern": "Can you give me a brief introduction to this {object}?",
            "variables": {"object": OBJECT},
            "category": "repository_intro",
        },
        {
            "pattern": "What is the main idea behind this {object}?",
            "variables": {"object": OBJECT},
            "category": "main_idea",
        },
        {
            "pattern": "What is this {object} built for?",
            "variables": {"object": OBJECT},
            "category": "built_for",
        },
        {
            "pattern": "Help me understand this {object} as a whole.",
            "variables": {"object": OBJECT},
            "category": "overall_understanding",
        },
        {
            "pattern": "Before I explore the code, explain this {object}.",
            "variables": {"object": OBJECT},
            "category": "before_reading",
        },
        {
            "pattern": "I am new to this {object}. Can you explain it?",
            "variables": {"object": OBJECT},
            "category": "new_developer",
        },
        {
            "pattern": "Give me a quick summary of this {object}.",
            "variables": {"object": OBJECT},
            "category": "quick_summary",
        },
        {
            "pattern": "Explain this {object} like I'm joining the project today.",
            "variables": {"object": OBJECT},
            "category": "beginner",
        },
        {
            "pattern": "What should I know about this {object} before reading the code?",
            "variables": {"object": OBJECT},
            "category": "repository_understanding",
        },
        {
            "pattern": "Can you provide some context about this {object}?",
            "variables": {"object": OBJECT},
            "category": "project_context",
        },
        {"pattern": "What business problem does this project solve?"},
        {"pattern": "Why was this application created?"},
        {"pattern": "What real-world need does this software address?"},
        {"pattern": "Who is the intended user of this application?"},
        {"pattern": "Who would typically use this software?"},
        {"pattern": "What type of users is this project designed for?"},
        {"pattern": "What does this repository cover?"},
        {"pattern": "What parts of the system are included in this repository?"},
        {"pattern": "What is inside this project?"},
        {"pattern": "What are the major features of this application?"},
        {"pattern": "What functionality does this project provide?"},
        {"pattern": "What can this software do?"},
        {"pattern": "Where should I begin learning this repository?"},
        {"pattern": "Which part should a beginner understand first?"},
        {"pattern": "What is the best starting point for understanding this project?"},
        {"pattern": "Describe this project in one paragraph."},
        {"pattern": "Summarize the repository in a few sentences."},
        {"pattern": "Give me the big picture of this project."},
        {"pattern": "Is this project production ready?"},
        {"pattern": "Does this repository look like a prototype or a mature system?"},
        {"pattern": "How complete is this project?"},
        {"pattern": "How complex is this repository?"},
        {"pattern": "Would this be considered a beginner or advanced project?"},
        {"pattern": "How difficult is this project to understand?"},
        {"pattern": "What should I know before contributing?"},
        {"pattern": "How can a new developer start contributing?"},
        {"pattern": "What should contributors understand first?"},
        {"pattern": "What is the primary objective of this repository?"},
        {"pattern": "What is this project ultimately trying to achieve?"},
        {"pattern": "What is the main goal of this software?"},
        {"pattern": "What makes this project useful?"},
        {"pattern": "Why would someone choose to use this application?"},
        {"pattern": "What value does this software provide?"},
                                            
        {"pattern": "Can you help me get oriented in this repository?"},
        {"pattern": "I'm unfamiliar with this codebase. Where do I begin?"},
        {
            "pattern": "Help me understand the overall structure before diving into the code."
        },
                                            
        {"pattern": "What is this application capable of doing?"},
        {"pattern": "What kind of tasks does this software perform?"},
        {"pattern": "What problems can users solve using this project?"},
                                         
        {"pattern": "How does this application work at a high level?"},
        {"pattern": "Can you explain the overall workflow of this project?"},
        {"pattern": "What happens from start to finish when using this application?"},
                                          
        {
            "pattern": "If you had to introduce this repository to someone, what would you say?"
        },
        {"pattern": "How would you describe this project to another developer?"},
        {"pattern": "What is the idfeature of this repository?"},
                                    
        {"pattern": "What domain does this application belong to?"},
        {"pattern": "What category of software is this project?"},
        {"pattern": "What type of application is this repository building?"},
                                           
        {
            "pattern": "Help me understand this repository before looking at the implementation."
        },
        {"pattern": "Explain the project without going into code details."},
        {"pattern": "Give me a conceptual understanding of this application."},
                                      
        {"pattern": "What should I notice first about this repository?"},
        {"pattern": "What stands out about this project?"},
        {"pattern": "What is the first thing a developer should understand here?"},
                                          
        {"pattern": "What is this repository trying to accomplish?"},
        {"pattern": "What is the end goal of this application?"},
        {"pattern": "What is the mission of this project?"},
        {"pattern": "Give me an executive summary of this repository."},
        {"pattern": "Summarize this project for a technical lead."},
        {"pattern": "Provide a concise executive overview of this application."},
    ],
                                
                  
                                
    "architecture": [
        {
            "pattern": "Explain the architecture of this application.",
            "category": "overall_architecture",
        },
        {
            "pattern": "How does {feature} interact with other features?",
            "variables": {"feature": FEATURES},
            "category": "interaction",
        },
        {
            "pattern": "Explain the flow of {feature}.",
            "variables": {"feature": FEATURES},
            "category": "flow",
        },
        {
            "pattern": "How does {feature} communicate with the rest of the system?",
            "variables": {"feature": FEATURES},
            "category": "communication",
        },
        {
            "pattern": "What features does {feature} depend on?",
            "variables": {"feature": FEATURES},
            "category": "dependency",
        },
        {
            "pattern": "Describe the lifecycle of {feature}.",
            "variables": {"feature": FEATURES},
            "category": "lifecycle",
        },
        {
            "pattern": "Describe the system design behind {feature}.",
            "variables": {"feature": FEATURES},
            "category": "system_design",
        },
        {
            "pattern": "How does data flow through {feature}?",
            "variables": {"feature": FEATURES},
            "category": "data_flow",
        },
        {
            "pattern": "How is {feature} connected to the rest of the repository?",
            "variables": {"feature": FEATURES},
            "category": "relationships",
        },
        {
            "pattern": "Give me the high-level design of {feature}.",
            "variables": {"feature": FEATURES},
            "category": "high_level_design",
        },
        {
            "category": "request_flow",
            "pattern": [
                "How does a request flow through the application?",
                "What path does a user request follow inside the system?",
                "Describe the request lifecycle in this project.",
                "How is an incoming request processed?",
                "Explain the request handling pipeline.",
            ],
        },
        {
            "category": "data_flow",
            "pattern": [
                "How does data move across the application?",
                "Describe the data flow of this system.",
                "How is information transferred between modules?",
                "Explain the movement of data inside the project.",
                "How does data travel through the architecture?",
            ],
        },
        {
            "category": "layered_design",
            "pattern": [
                "How is this application divided into layers?",
                "Describe the layered architecture of this repository.",
                "How are responsibilities separated across layers?",
                "Explain the architectural layers of this project.",
                "What layers exist in this application?",
            ],
        },
        {
            "category": "feature_responsibilities",
            "pattern": [
                "How are responsibilities distributed across features?",
                "Which features own which responsibilities?",
                "How is responsibility separation achieved?",
                "Explain how different modules divide their work.",
                "How are architectural responsibilities assigned?",
            ],
        },
        {
            "category": "frontend_backend_communication",
            "pattern": [
                "How do the frontend and backend communicate?",
                "Explain communication between the client and the server.",
                "How are requests exchanged between frontend and backend?",
                "Describe the interaction between the UI and the server.",
                "How is client-server communication organized?",
            ],
        },
        {
            "category": "design_decisions",
            "pattern": [
                "Why is the architecture designed this way?",
                "What architectural decisions shaped this project?",
                "What design choices define this repository?",
                "Explain the reasoning behind the architecture.",
                "Why was this architecture chosen?",
            ],
        },
        {
            "category": "module_boundaries",
            "pattern": [
                "How are module boundaries defined?",
                "Where does one subsystem end and another begin?",
                "How are different parts of the system isolated?",
                "Explain subsystem boundaries.",
                "How are architectural boundaries maintained?",
            ],
        },
        {
            "category": "coupling",
            "pattern": [
                "How tightly coupled are the modules?",
                "How independent are the system features?",
                "Describe coupling in this architecture.",
                "How dependent are modules on each other?",
                "How does the architecture reduce coupling?",
            ],
        },
        {
            "category": "scalability",
            "pattern": [
                "Can this architecture scale easily?",
                "How scalable is the overall design?",
                "Would this architecture support future growth?",
                "How does the architecture handle scaling?",
                "Explain scalability from an architectural perspective.",
            ],
        },
        {
            "category": "extensibility",
            "pattern": [
                "How easy is it to extend this architecture?",
                "Can new features be added without major changes?",
                "How flexible is the current design?",
                "How extensible is the repository structure?",
                "Explain how the architecture supports future development.",
            ],
        },
        {
            "category": "system_organization",
            "pattern": [
                "How is the system organized internally?",
                "Describe the overall organization of the repository.",
                "How are architectural features arranged?",
                "Explain the organizational structure of the application.",
                "How is the project structured internally?",
            ],
        },
        {
            "category": "architectural_pattern",
            "pattern": [
                "Which architectural pattern does this project follow?",
                "What design pattern best describes this architecture?",
                "How would you classify the architectural style?",
                "Does this repository follow a layered or modular architecture?",
                "Explain the architectural pattern used.",
            ],
        },
        {
            "category": "application_lifecycle",
            "pattern": [
                "How does the application start and initialize?",
                "Describe the startup lifecycle.",
                "What happens when the application boots?",
                "Explain the initialization process.",
                "How is the application lifecycle organized?",
            ],
        },
        {
            "category": "dependency_direction",
            "pattern": [
                "How do dependencies flow across the architecture?",
                "Which direction do architectural dependencies follow?",
                "Explain dependency flow in the project.",
                "How are dependencies organized?",
                "Describe the dependency hierarchy.",
            ],
        },
        {
            "category": "big_picture_architecture",
            "pattern": [
                "Give me the big-picture architecture.",
                "Describe the architecture from a bird's-eye view.",
                "Explain the entire system architecture.",
                "Summarize the architectural design.",
                "What does the complete architecture look like?",
            ],
        },
        {
            "pattern": [
                "How does {feature} fit into the overall system?",
                "How does {feature} interact with other features?",
                "How does {feature} connect to the rest of the application?",
                "What role does {feature} play in the overall architecture?",
                "How does data flow through {feature} across the system?",
                "How is {feature} connected to other parts of the application?",
                "What dependencies does {feature} have within the system?",
                "How does {feature} participate in the overall request flow?",
                "Where does {feature} fit within the system design?",
                "How does {feature} communicate with other features?",
            ],
            "variables": {"feature": FEATURES},
            "category": "high_level_design",
        },
        {
            "pattern": [
                                             
                "How does data flow across {feature} and the rest of the system?",
                "How does information move between {feature} and other features?",
                "Describe how {feature} participates in the system's data flow.",
                "How does data travel through the architecture involving {feature}?",
                "What is the system-level data flow around {feature}?",
                                  
                "What design decisions shape the architecture of {feature}?",
                "Why was {feature} designed this way within the system?",
                "What architectural choices influence {feature}?",
                "What design principles define how {feature} fits into the application?",
                "How do the design decisions around {feature} affect the overall system?",
                                           
                "How are responsibilities separated around {feature}?",
                "What responsibilities belong to {feature} compared with other parts of the system?",
                "How does {feature} contribute to the separation of concerns?",
                "How are responsibilities distributed between {feature} and other modules?",
                "What architectural responsibility does {feature} have?",
                               
                "What role does {feature} serve in the system architecture?",
                "Why does {feature} exist as a separate part of the application?",
                "How does {feature} fit into the application's architectural design?",
                "What place does {feature} have in the overall system structure?",
                "How is the role of {feature} defined within the architecture?",
            ],
            "variables": {"feature": FEATURES},
            "category": "high_level_design",
        },
    ],
                                
                    
                                
    "implementation": [
        {
            "pattern": "How is {feature} implemented?",
            "variables": {"feature": FEATURES},
            "category": "implementation",
        },
        {
            "pattern": "Explain how {feature} works.",
            "variables": {"feature": FEATURES},
            "category": "explanation",
        },
        {
            "pattern": "Walk me through the implementation of {feature}.",
            "variables": {"feature": FEATURES},
            "category": "walkthrough",
        },
        {
            "pattern": "Explain the internal logic of {feature}.",
            "variables": {"feature": FEATURES},
            "category": "logic",
        },
        {
            "pattern": "Explain the execution flow of {feature}.",
            "variables": {"feature": FEATURES},
            "category": "execution",
        },
        {
            "pattern": "Help me understand the code behind {feature}.",
            "variables": {"feature": FEATURES},
            "category": "code",
        },
        {
            "pattern": "Explain {feature} step by step.",
            "variables": {"feature": FEATURES},
            "category": "step_by_step",
        },
        {
            "pattern": "Teach me how {feature} works.",
            "variables": {"feature": FEATURES},
            "category": "learning",
        },
        {
            "pattern": "How was {feature} built?",
            "variables": {"feature": FEATURES},
            "category": "build",
        },
        {
            "pattern": "Explain the implementation of the {feature} module.",
            "variables": {"feature": FEATURES},
            "category": "module",
        },
        {
            "category": "behind_scenes",
            "pattern": "What happens behind the scenes when {feature} runs?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "under_the_hood",
            "pattern": "How does {feature} work under the hood?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "deep_dive",
            "pattern": "Can you do a deep dive into {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "mechanism",
            "pattern": "Explain the mechanism behind {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "working_principle",
            "pattern": "Explain the working principle of {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "processing",
            "pattern": "How does {feature} process requests?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "request_lifecycle",
            "pattern": "What happens after {feature} receives a request?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "sequence",
            "pattern": "What is the sequence of operations inside {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "input_output",
            "pattern": "How does {feature} transform input into output?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "lifecycle",
            "pattern": "Describe the lifecycle of {feature} during execution.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "reasoning",
            "pattern": "Why is {feature} implemented this way?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "algorithm",
            "pattern": "Explain the algorithm used in {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "event_handling",
            "pattern": "How does {feature} handle events internally?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "state_changes",
            "pattern": "How does the internal state change during {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "end_to_end",
            "pattern": "Explain the complete execution of {feature} from start to finish.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "end_to_end",
            "pattern": [
                "How does {feature} work internally?",
                "What happens internally when {feature} runs?",
                "How does {feature} process data internally?",
                "What steps does {feature} perform internally?",
                "How is the logic of {feature} executed?",
                "What happens behind the scenes inside {feature}?",
                "How does {feature} handle its internal operations?",
                "How is {feature} implemented internally?",
                "What is the internal workflow of {feature}?",
                "How does {feature} transform its input internally?",
            ],
            "variables": {"feature": FEATURES},
        },
    ],
                                
            
                               
    "locate": [
        {
            "category": "where",
            "pattern": "Where is {feature} implemented?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "locate",
            "pattern": "Locate {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "find",
            "pattern": "Find {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "which_file",
            "pattern": "Which file contains {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "which_module",
            "pattern": "Which module handles {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "folder",
            "pattern": "Which folder contains {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "feature",
            "pattern": "Which feature is responsible for {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "defined",
            "pattern": "Where is {feature} defined?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "declared",
            "pattern": "Where is {feature} declared?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "used",
            "pattern": "Where is {feature} used?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "lives",
            "pattern": "Where does {feature} live?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "point_me",
            "pattern": "Point me to the implementation of {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "navigation",
            "pattern": "Take me to {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "function",
            "pattern": "Which function handles {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "class",
            "pattern": "Which class is responsible for {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "configuration_files",
            "pattern": [
                "Where is the configuration for {feature} located?",
                "Which configuration file contains {feature}?",
                "Where can I find the configuration related to {feature}?",
                "Which config manages {feature}?",
                "Locate the configuration for {feature}.",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "environment_variables",
            "pattern": [
                "Where are the environment variables for {feature} defined?",
                "Which environment variable controls {feature}?",
                "Locate the env configuration for {feature}.",
                "Where is the environment setup for {feature}?",
                "Find the environment settings related to {feature}.",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "api_routes",
            "pattern": [
                "Which API route handles {feature}?",
                "Where is the route for {feature} defined?",
                "Locate the endpoint for {feature}.",
                "Which route is responsible for {feature}?",
                "Find the API responsible for {feature}.",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "database_models",
            "pattern": [
                "Which model represents {feature}?",
                "Where is the database model for {feature}?",
                "Locate the schema used by {feature}.",
                "Which collection stores {feature}?",
                "Find the model associated with {feature}.",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "controllers",
            "pattern": [
                "Which controller handles {feature}?",
                "Where is the controller for {feature}?",
                "Locate the controller responsible for {feature}.",
                "Find the controller managing {feature}.",
                "Which controller implements {feature}?",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "services",
            "pattern": [
                "Which service implements {feature}?",
                "Where is the service for {feature}?",
                "Locate the business logic of {feature}.",
                "Which service manages {feature}?",
                "Find the service responsible for {feature}.",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "middleware_registration",
            "pattern": [
                "Where is the middleware for {feature} registered?",
                "Which middleware handles {feature}?",
                "Locate middleware related to {feature}.",
                "Find the middleware responsible for {feature}.",
                "Where can I see the middleware configuration for {feature}?",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "utility_functions",
            "pattern": [
                "Which utility function supports {feature}?",
                "Where are helper functions for {feature}?",
                "Locate utilities related to {feature}.",
                "Find helper code used by {feature}.",
                "Where are shared utilities for {feature}?",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "constants",
            "pattern": [
                "Where are constants for {feature} defined?",
                "Locate constants related to {feature}.",
                "Which file contains constants used by {feature}?",
                "Find configuration constants for {feature}.",
                "Where are reusable constants for {feature}?",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "startup_files",
            "pattern": [
                "Where is {feature} initialized?",
                "Which startup file loads {feature}?",
                "Locate the initialization code for {feature}.",
                "Where does {feature} get registered during startup?",
                "Find where {feature} is first initialized.",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "startup_files",
            "pattern": [
                "Where is {feature} implemented?",
                "Which file contains the implementation of {feature}?",
                "Which module contains {feature}?",
                "Where can I find the code for {feature}?",
                "Which function handles {feature}?",
                "Which service implements {feature}?",
                "Where is the controller for {feature}?",
                "Which file is responsible for {feature}?",
                "Point me to the code for {feature}.",
                "Where can I find the implementation of {feature}?",
            ],
            "variables": {"feature": FEATURES},
        },
        {
            "category": "startup_files",
            "pattern": [
                                                                            
                "Point me to the implementation of {feature}.",
                "Where can I find the implementation of {feature}?",
                "Locate the implementation code for {feature}.",
                "Show me where {feature} is implemented.",
                "Which file contains the implementation of {feature}?",
                                       
                "Where can I find the internal logic of {feature}?",
                "Point me to the code behind {feature}.",
                "Locate the logic responsible for {feature}.",
                "Which file contains the logic for {feature}?",
                "Show me where the internal code for {feature} is located.",
                                                         
                "Where is the architecture for {feature} defined?",
                "Point me to the code that defines the architecture of {feature}.",
                "Which file defines the structure of {feature}?",
                "Where can I locate the design-related code for {feature}?",
                "Show me where the system structure for {feature} is defined.",
            ],
            "variables": {"feature": FEATURES},
        },
    ],
                                
                
                               
    "comparison": [
        {
            "category": "compare",
            "pattern": "Compare {feature1} and {feature2}.",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "difference",
            "pattern": "What is the difference between {feature1} and {feature2}?",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "similarities",
            "pattern": "How are {feature1} and {feature2} similar?",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "contrast",
            "pattern": "Contrast {feature1} with {feature2}.",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "versus",
            "pattern": "{feature1} vs {feature2}.",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "side_by_side",
            "pattern": "Explain {feature1} and {feature2} side by side.",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "better",
            "pattern": "Which is better, {feature1} or {feature2}?",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "tradeoffs",
            "pattern": "What are the tradeoffs between {feature1} and {feature2}?",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "pros_cons",
            "pattern": "Compare the pros and cons of {feature1} and {feature2}.",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "use_case",
            "pattern": "When should I use {feature1} instead of {feature2}?",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "performance",
            "pattern": "How do {feature1} and {feature2} differ in terms of performance?",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "responsibility",
            "pattern": "How are the responsibilities of {feature1} and {feature2} different?",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "roles",
            "pattern": "Compare the roles of {feature1} and {feature2}.",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "internal_design",
            "pattern": "How do the implementations of {feature1} and {feature2} differ?",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "architecture",
            "pattern": "Compare the architecture of {feature1} and {feature2}.",
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
        {
            "category": "architecture",
            "pattern": [
                "How does {feature1} differ from {feature2}?",
                "What are the differences between {feature1} and {feature2}?",
                "How do {feature1} and {feature2} compare?",
                "Which responsibilities belong to {feature1} versus {feature2}?",
                "What is different about {feature1} and {feature2}?",
                "How are {feature1} and {feature2} different in the system?",
                "Compare the roles of {feature1} and {feature2}.",
                "How do the responsibilities of {feature1} and {feature2} differ?",
            ],
            "variables": {"feature1": FEATURES, "feature2": FEATURES},
            "symmetric": True,
        },
    ],
                                
                               
           
                               
    "debug": [
        {
            "category": "not_working",
            "pattern": "Why is {feature} not working?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "failing",
            "pattern": "Why is {feature} failing?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "broken",
            "pattern": "{feature} seems broken.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "crashing",
            "pattern": "{feature} keeps crashing.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "unexpected",
            "pattern": "Why is {feature} behaving unexpectedly?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "issue",
            "pattern": "There is an issue with {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "debug",
            "pattern": "Help me debug {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "diagnose",
            "pattern": "Diagnose the problem with {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "fix",
            "pattern": "How can I fix {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "root_cause",
            "pattern": "Find the root cause of the problem in {feature}.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "always",
            "pattern": "{feature} always fails.",
            "variables": {"feature": FEATURES},
        },
                              
        {
            "category": "never",
            "pattern": "{feature} never works.",
            "variables": {"feature": FEATURES},
        },
                                
        {
            "category": "does_not",
            "pattern": "{feature} doesn't work anymore.",
            "variables": {"feature": FEATURES},
        },
                              
        {
            "category": "stops",
            "pattern": "{feature} suddenly stopped working.",
            "variables": {"feature": FEATURES},
        },
                                          
        {
            "category": "wrong_output",
            "pattern": "{feature} returns incorrect results.",
            "variables": {"feature": FEATURES},
        },
                                        
        {
            "category": "wrong_behaviour",
            "pattern": "{feature} behaves differently than expected.",
            "variables": {"feature": FEATURES},
        },
                                        
        {
            "category": "nothing_happens",
            "pattern": "Nothing happens when I use {feature}.",
            "variables": {"feature": FEATURES},
        },
                              
        {
            "category": "stuck",
            "pattern": "{feature} gets stuck.",
            "variables": {"feature": FEATURES},
        },
                                 
        {
            "category": "infinite",
            "pattern": "{feature} runs forever.",
            "variables": {"feature": FEATURES},
        },
                                
        {
            "category": "timeout",
            "pattern": "{feature} keeps timing out.",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "exception",
            "pattern": "Why is {feature} throwing an exception?",
            "variables": {"feature": FEATURES},
        },
                             
        {
            "category": "error",
            "pattern": "Why does {feature} throw an error?",
            "variables": {"feature": FEATURES},
        },
                            
        {
            "category": "null",
            "pattern": "Why is {feature} returning null?",
            "variables": {"feature": FEATURES},
        },
                                 
        {
            "category": "undefined",
            "pattern": "Why is {feature} returning undefined?",
            "variables": {"feature": FEATURES},
        },
                               
        {
            "category": "missing_data",
            "pattern": "Why is {feature} missing data?",
            "variables": {"feature": FEATURES},
        },
                                      
        {
            "category": "incorrect_data",
            "pattern": "Why is {feature} producing incorrect data?",
            "variables": {"feature": FEATURES},
        },
                                  
        {
            "category": "validation",
            "pattern": "Why is validation failing in {feature}?",
            "variables": {"feature": FEATURES},
        },
                                   
        {
            "category": "api_failure",
            "pattern": "Why is the API failing in {feature}?",
            "variables": {"feature": FEATURES},
        },
                               
        {
            "category": "request",
            "pattern": "Why does the request fail in {feature}?",
            "variables": {"feature": FEATURES},
        },
                                
        {
            "category": "response",
            "pattern": "Why is the response incorrect in {feature}?",
            "variables": {"feature": FEATURES},
        },
        {
            "category": "trace_execution",
            "pattern": "Trace the execution of {feature}.",
            "variables": {"feature": FEATURES},
        },
                                  
        {
            "category": "investigation",
            "pattern": "Investigate the issue in {feature}.",
            "variables": {"feature": FEATURES},
        },
                                 
        {
            "category": "root_cause_analysis",
            "pattern": "Help me identify the root cause in {feature}.",
            "variables": {"feature": FEATURES},
        },
                              
        {
            "category": "logging",
            "pattern": "Where should I add logs to debug {feature}?",
            "variables": {"feature": FEATURES},
        },
                                          
        {
            "category": "state",
            "pattern": "Help me investigate the state changes in {feature}.",
            "variables": {"feature": FEATURES},
        },
                                 
        {
            "category": "bottleneck",
            "pattern": "Find the bottleneck in {feature}.",
            "variables": {"feature": FEATURES},
        },
                                        
        {
            "category": "performance",
            "pattern": "Why is {feature} performing poorly?",
            "variables": {"feature": FEATURES},
        },
                                     
        {
            "category": "race_condition",
            "pattern": "Could {feature} have a race condition?",
            "variables": {"feature": FEATURES},
        },
                                  
        {
            "category": "memory",
            "pattern": "Does {feature} have a memory leak?",
            "variables": {"feature": FEATURES},
        },
                                
        {
            "category": "reproduce",
            "pattern": "Help me reproduce the bug in {feature}.",
            "variables": {"feature": FEATURES},
        },
    ],
                               
            
                               
    "casual": [
        {"category": "greeting", "pattern": "Hello"},
                       
        {"category": "greeting", "pattern": "Hi"},
                                 
        {"category": "greeting", "pattern": "Good morning"},
                            
        {"category": "goodbye", "pattern": "Goodbye"},
                           
        {"category": "thanks", "pattern": "Thank you"},
                                 
        {"category": "appreciation", "pattern": "That was helpful."},
                              
        {"category": "idfeature", "pattern": "Who are you?"},
                               
        {"category": "capability", "pattern": "What can you do?"},
                         
        {"category": "help", "pattern": "Can you help me?"},
                          
        {"category": "joke", "pattern": "Tell me a joke."},
                                  
        {"category": "confirmation", "pattern": "Okay"},
                                     
        {"category": "acknowledgement", "pattern": "Got it."},
                          
        {"category": "reaction", "pattern": "Nice!"},
                                 
        {"category": "small_talk", "pattern": "How are you?"},
                         
        {"category": "bye", "pattern": "See you later."},
        {
            "category": "greeting",
            "pattern": ["Hi", "Hello", "Hey", "Greetings", "Hi there"],
        },
        {
            "category": "morning_greeting",
            "pattern": [
                "Good morning",
                "Morning!",
                "Hope you're having a good morning.",
                "Morning mentor!",
                "Good morning, how are you?",
            ],
        },
        {
            "category": "evening_greeting",
            "pattern": [
                "Good evening",
                "Evening!",
                "Hope you're having a good evening.",
                "Good evening mentor.",
                "Evening, how's it going?",
            ],
        },
        {
            "category": "farewell",
            "pattern": [
                "Bye",
                "See you later",
                "Goodbye",
                "Catch you later",
                "Talk to you soon",
            ],
        },
        {
            "category": "gratitude",
            "pattern": [
                "Thank you",
                "Thanks",
                "Thanks a lot",
                "Really appreciate it",
                "Much appreciated",
            ],
        },
        {
            "category": "appreciation",
            "pattern": [
                "Nice work",
                "Great explanation",
                "That was helpful",
                "Excellent answer",
                "Well explained",
            ],
        },
        {
            "category": "compliment",
            "pattern": [
                "You're amazing",
                "You're a great teacher",
                "You're really helpful",
                "You're awesome",
                "You're brilliant",
            ],
        },
        {
            "category": "agreement",
            "pattern": ["Okay", "Sounds good", "Makes sense", "Got it", "Alright"],
        },
        {
            "category": "confirmation",
            "pattern": [
                "Understood",
                "I understand",
                "That makes sense",
                "Crystal clear",
                "Everything is clear now",
            ],
        },
        {
            "category": "confusion",
            "pattern": [
                "I'm confused",
                "I don't understand",
                "Can you explain again?",
                "This doesn't make sense.",
                "I'm lost.",
            ],
        },
        {
            "category": "idfeature",
            "pattern": [
                "Who are you?",
                "Tell me about yourself.",
                "What are you?",
                "Who am I talking to?",
                "Introduce yourself.",
            ],
        },
        {
            "category": "capabilities",
            "pattern": [
                "What can you do?",
                "How can you help me?",
                "What are your capabilities?",
                "What can I ask you?",
                "How can you assist me?",
            ],
        },
        {
            "category": "help",
            "pattern": [
                "Help me",
                "I need help",
                "Can you help me?",
                "Please help",
                "I need some assistance",
            ],
        },
        {
            "category": "encouragement",
            "pattern": [
                "Let's do this",
                "We can do it",
                "Keep going",
                "Let's continue",
                "Let's move forward",
            ],
        },
        {
            "category": "excitement",
            "pattern": [
                "Awesome!",
                "Wow!",
                "Amazing!",
                "That's exciting!",
                "Fantastic!",
            ],
        },
        {
            "category": "positive_feedback",
            "pattern": [
                "You're doing great",
                "You're helping a lot",
                "This project is exciting",
                "This is really useful.",
                "I'm learning a lot",
            ],
        },
        {
            "category": "conversation",
            "pattern": [
                "How are you?",
                "How's it going?",
                "Hope you're doing well.",
                "What's up?",
                "Everything good?",
            ],
        },
        {
            "category": "politeness",
            "pattern": [
                "Please",
                "If you don't mind",
                "Would you kindly help me?",
                "Could you please help?",
                "Please guide me.",
            ],
        },
        {
            "category": "apology",
            "pattern": [
                "Sorry",
                "My mistake",
                "I apologize",
                "Sorry about that",
                "Oops, my bad",
            ],
        },
        {
            "category": "random_chat",
            "pattern": [
                "Tell me something interesting.",
                "Tell me a joke.",
                "Let's chat.",
                "Let's talk.",
                "Say something fun.",
            ],
        },
        {
            "category": "random_chat",
            "pattern": [
                "This is really helpful.",
                "This is really useful.",
                "That was helpful.",
                "That is useful.",
                "This helped me a lot.",
                "I understand now.",
                "Got it.",
                "I get it now.",
                "That makes things clearer.",
                "That cleared up my confusion.",
                "This is exactly what I needed.",
                "That's great.",
                "Awesome work.",
                "Perfect.",
                "Great, thanks.",
                "Thank you, that helped.",
                "I appreciate the help.",
                "Nice explanation.",
                "That was a good explanation.",
                "This makes much more sense now.",
                "I'm excited to continue.",
                "Let's keep going.",
                "I'm ready for the next step.",
                "Okay, let's continue.",
                "Yes, let's move forward.",
                "Alright, what's next?",
                "Cool, let's do it.",
            ],
        },
    ],
}
