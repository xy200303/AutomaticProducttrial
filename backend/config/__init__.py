import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """配置数据模型"""
    just_one_api_key: str
    dashscope_api_key: str

    @classmethod
    def from_yaml(cls, yaml_path: str = "config.yaml") -> "Config":
        """从YAML文件加载配置

        Args:
            yaml_path: YAML配置文件路径

        Returns:
            Config实例

        Raises:
            FileNotFoundError: 当配置文件不存在时
            yaml.YAMLError: 当YAML文件格式错误时
            KeyError: 当缺少必需的配置项时
        """
        config_path = Path(yaml_path)

        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {yaml_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML文件格式错误: {e}")

        if not data or 'JustOneApiKey' not in data:
            raise KeyError("配置文件缺少必需的 'JustOneApiKey' 字段")

        return cls(
            just_one_api_key=data['JustOneApiKey'],
            dashscope_api_key=data["DashscopeApiKey"]
        )

    def get_api_key(self) -> str:
        """获取API密钥

        Returns:
            API密钥字符串
        """
        return self.just_one_api_key


# 全局配置实例
_config_instance: Optional[Config] = None


def load_config(yaml_path: str = "config.yaml") -> Config:
    """加载配置文件

    Args:
        yaml_path: YAML配置文件路径

    Returns:
        Config实例
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config.from_yaml(yaml_path)
    return _config_instance


def get_config() -> Config:
    """获取已加载的配置实例

    Returns:
        Config实例

    Raises:
        RuntimeError: 当配置尚未加载时
    """
    if _config_instance is None:
        raise RuntimeError("配置尚未加载，请先调用 load_config()")
    return _config_instance


def reload_config(yaml_path: str = "config.yaml") -> Config:
    """重新加载配置文件

    Args:
        yaml_path: YAML配置文件路径

    Returns:
        新的Config实例
    """
    global _config_instance
    _config_instance = Config.from_yaml(yaml_path)
    return _config_instance


Config = load_config()