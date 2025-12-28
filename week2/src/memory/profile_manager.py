import json
import os
from models import UserProfile

class UserProfileManager:
    def __init__(self, filepath="week2/user_data.json"):
        self.filepath = filepath
        if not os.path.exists(filepath):
            # 初始化一个空对象的 JSON
            self._save_data(UserProfile().model_dump())
            
    def _save_data(self, data: dict):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_profile(self) -> dict:
        """加载原始字典数据"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def update_profile(self, new_profile: UserProfile):
        """
        合并逻辑：将新提取的非空字段，覆盖旧数据
        """
        current_dict = self.load_profile()
        new_dict = new_profile.model_dump()
        
        # 简单的合并逻辑：只有当新值不为空时才更新
        for key, value in new_dict.items():
            if value: # 如果提取到了新值 (非 None, 非空 list)
                # 对于列表，我们采用 append 模式而不是覆盖 (可选)
                if isinstance(value, list):
                    current_list = current_dict.get(key, [])
                    # 去重合并
                    merged_list = list(set(current_list + value))
                    current_dict[key] = merged_list
                else:
                    current_dict[key] = value
                    
        self._save_data(current_dict)
        return current_dict