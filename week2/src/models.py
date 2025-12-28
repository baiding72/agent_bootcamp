from pydantic import BaseModel, Field
from typing import Optional, List

# 这就像是你的 Java Entity/DTO
class UserProfile(BaseModel):
    name: Optional[str] = Field(description="用户的名字", default=None)
    job: Optional[str] = Field(description="用户的职业", default=None)
    interests: List[str] = Field(description="用户的兴趣爱好列表", default_factory=list)
    tech_stack: List[str] = Field(description="用户的技术栈", default_factory=list)
    
    # 作为一个合格的后端，我们要重写 toString (或者 dict) 方法方便存储
    def to_summary_string(self):
        return f"姓名:{self.name}, 职业:{self.job}, 兴趣:{', '.join(self.interests)}, 技术:{', '.join(self.tech_stack)}"