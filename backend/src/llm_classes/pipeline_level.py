from llm_level import *

class Stage(ABC):
    def __init__(self):
        self.next = None
        self.input = None

    @abstractmethod
    def forward(self, inputs):
        pass

    @abstractmethod
    def process_inputs(self, inputs):
        pass

class LLMStage(Stage):
    def __init__(self, llm: LLM, process_function):
        self.llm = llm
        self.process_function = process_function # function that processes text by doing prompt engineering
        super().__init__()
    
    def forward(self, inputs: str) -> str:
        return self.llm.run(self.process_inputs(inputs))

    def process_inputs(self, inputs: str) -> list:
        '''
        Converts string into json array format for feeding into llm. Also processes text aka perform prompt engineering
        '''
        out = self.process_function(inputs)
        # Still needs stuff
        return out # messages

class Pipeline:
    def __init__(self, *list_of_stages, start_index=0):
        self.list_of_stages = list_of_stages
        self.current_index = start_index

    def run(self, initial_input: list):
        '''
        Gets output from the stage, decide whether to continue conversation chain, add new stage and update pointer,
        or if the user is editing a reply, set pointer to the stage the index has updated and delete all after.
        '''
        # use self.list_of_stages[current_index].forward()
        return




        