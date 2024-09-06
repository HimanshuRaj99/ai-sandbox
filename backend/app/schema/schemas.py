from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ConfigRequest(BaseModel):
    provider: str
    model: str
    character: str
    grade: int
    version: str
    standard: str

class FindMeaningRequest(BaseModel):
    selected_characters: str
    context: str
    grade: str
class ClickRevealRequest(BaseModel):
    word: str
    grade: int
    model:str

class ChatResponse(BaseModel):
    response: str

class ClickPronounceResponse(BaseModel):
    status: bool

class ClickPronounceRequest(BaseModel):
    word: str

class ActivityRequest(BaseModel):
    type: str
    content: str

class GenerateSVPQuiz(BaseModel):
    paragraph: str
    gradeLevel: int
    model: str
    standard: str
    numQuestions: int

class GenerateSequenceStory(BaseModel):
    topic: str
    gradeLevel: int
    model: str

class SimplifyMeaningRequest(BaseModel):
    text: str
    context: str
    grade: str
    generated_meaning: str