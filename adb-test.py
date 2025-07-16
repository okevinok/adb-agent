from ppadb.client import Client
import time
import json
from typing import Dict, Any, Optional, Tuple

class AndroidDevice:
    def __init__(self, host='127.0.0.1', port=5037):
        """初始化 ADB 连接"""
        self.adb = Client(host=host, port=port)
        self.device = None
        self.connect()

    def connect(self):
        """连接设备"""
        try:
            devices = self.adb.devices()
            if not devices:
                raise Exception("未检测到已连接的设备")
            self.device = devices[0]
            print("设备连接成功")
        except Exception as e:
            print(f"连接失败: {str(e)}")
            exit(1)

    def get_screen_size(self) -> Dict[str, Any]:
        """
        MCP工具: 获取屏幕分辨率
        
        Returns:
            Dict[str, Any]: 包含成功状态和屏幕尺寸信息
        """
        try:
            output = self.device.shell("wm size").strip()
            size_str = output.split(":")[1].strip()
            width, height = map(int, size_str.split("x"))
            return {
                "success": True,
                "width": width,
                "height": height,
                "message": f"屏幕分辨率: {width}x{height}"
            }
        except Exception as e:
            return {
                "success": False,
                "width": None,
                "height": None,
                "message": f"获取屏幕分辨率失败: {str(e)}"
            }

    def tap(self, x: int, y: int) -> Dict[str, Any]:
        """
        MCP工具: 在屏幕指定坐标点击
        
        Args:
            x (int): X坐标
            y (int): Y坐标
            
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        try:
            self.device.shell(f"input tap {x} {y}")
            return {
                "success": True,
                "action": "tap",
                "coordinates": {"x": x, "y": y},
                "message": f"已点击坐标: ({x}, {y})"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "tap",
                "coordinates": {"x": x, "y": y},
                "message": f"点击失败: {str(e)}"
            }

    def long_press(self, x: int, y: int, duration: int = 1000) -> Dict[str, Any]:
        """
        MCP工具: 在屏幕指定坐标长按
        
        Args:
            x (int): X坐标
            y (int): Y坐标
            duration (int): 长按时长，单位毫秒，默认1000ms
            
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        try:
            self.device.shell(f"input swipe {x} {y} {x} {y} {duration}")
            return {
                "success": True,
                "action": "long_press",
                "coordinates": {"x": x, "y": y},
                "duration": duration,
                "message": f"已长按坐标: ({x}, {y})，时长: {duration}ms"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "long_press",
                "coordinates": {"x": x, "y": y},
                "duration": duration,
                "message": f"长按失败: {str(e)}"
            }

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 500) -> Dict[str, Any]:
        """
        MCP工具: 屏幕滑动操作
        
        Args:
            x1 (int): 起始X坐标
            y1 (int): 起始Y坐标
            x2 (int): 结束X坐标
            y2 (int): 结束Y坐标
            duration (int): 滑动时长，单位毫秒，默认500ms
            
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        try:
            self.device.shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")
            return {
                "success": True,
                "action": "swipe",
                "start_coordinates": {"x": x1, "y": y1},
                "end_coordinates": {"x": x2, "y": y2},
                "duration": duration,
                "message": f"已滑动: ({x1}, {y1}) -> ({x2}, {y2})，时长: {duration}ms"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "swipe",
                "start_coordinates": {"x": x1, "y": y1},
                "end_coordinates": {"x": x2, "y": y2},
                "duration": duration,
                "message": f"滑动失败: {str(e)}"
            }

    def input_text(self, text: str) -> Dict[str, Any]:
        """
        MCP工具: 输入指定文本
        
        Args:
            text (str): 要输入的文本内容
            
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        try:
            # 替换特殊字符以避免 ADB 命令错误
            original_text = text
            text = text.replace(" ", "%s").replace("&", "\\&").replace("|", "\\|")
            self.device.shell(f"input text '{text}'")
            return {
                "success": True,
                "action": "input_text",
                "original_text": original_text,
                "processed_text": text,
                "message": f"已输入文本: {original_text}"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "input_text",
                "original_text": text,
                "processed_text": "",
                "message": f"输入文本失败: {str(e)}"
            }

    def press_key(self, keycode: int) -> Dict[str, Any]:
        """
        MCP工具: 模拟按键事件
        
        Args:
            keycode (int): Android KeyEvent 代码
            
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        try:
            self.device.shell(f"input keyevent {keycode}")
            return {
                "success": True,
                "action": "press_key",
                "keycode": keycode,
                "message": f"已发送按键: {keycode}"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "press_key",
                "keycode": keycode,
                "message": f"按键发送失败: {str(e)}"
            }

    def back(self) -> Dict[str, Any]:
        """
        MCP工具: 模拟返回键
        
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        result = self.press_key(4)  # KEYCODE_BACK
        result["action"] = "back"
        result["message"] = result["message"].replace("按键: 4", "返回键")
        return result

    def home(self) -> Dict[str, Any]:
        """
        MCP工具: 模拟Home键
        
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        result = self.press_key(3)  # KEYCODE_HOME
        result["action"] = "home"
        result["message"] = result["message"].replace("按键: 3", "Home键")
        return result

    def power(self) -> Dict[str, Any]:
        """
        MCP工具: 模拟电源键
        
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        result = self.press_key(26)  # KEYCODE_POWER
        result["action"] = "power"
        result["message"] = result["message"].replace("按键: 26", "电源键")
        return result

    def click_and_input(self, x: int, y: int, text: str, delay: float = 0.5) -> Dict[str, Any]:
        """
        MCP工具: 点击输入框并输入字符（组合功能）
        
        Args:
            x (int): 输入框的X坐标
            y (int): 输入框的Y坐标
            text (str): 要输入的文本内容
            delay (float): 点击后等待时间，单位秒，默认0.5秒
            
        Returns:
            Dict[str, Any]: 包含操作结果和详细状态信息
        """
        try:
            # 先点击输入框
            tap_result = self.tap(x, y)
            if not tap_result["success"]:
                return {
                    "success": False,
                    "action": "click_and_input",
                    "step": "tap",
                    "coordinates": {"x": x, "y": y},
                    "text": text,
                    "message": f"点击输入框失败: {tap_result['message']}"
                }
            
            # 等待指定时间
            time.sleep(delay)
            
            # 输入文本
            input_result = self.input_text(text)
            if not input_result["success"]:
                return {
                    "success": False,
                    "action": "click_and_input",
                    "step": "input",
                    "coordinates": {"x": x, "y": y},
                    "text": text,
                    "message": f"输入文本失败: {input_result['message']}"
                }
            
            return {
                "success": True,
                "action": "click_and_input",
                "coordinates": {"x": x, "y": y},
                "text": text,
                "delay": delay,
                "tap_result": tap_result,
                "input_result": input_result,
                "message": f"已点击坐标({x}, {y})并输入文本: {text}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "action": "click_and_input",
                "coordinates": {"x": x, "y": y},
                "text": text,
                "message": f"点击输入框并输入字符失败: {str(e)}"
            }

    def clear_input_field(self, x: int, y: int) -> Dict[str, Any]:
        """
        MCP工具: 清空输入框内容（专用方法）
        
        Args:
            x (int): 输入框的X坐标
            y (int): 输入框的Y坐标
            
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        try:
            # 点击输入框获取焦点
            tap_result = self.tap(x, y)
            if not tap_result["success"]:
                return {
                    "success": False,
                    "action": "clear_input_field",
                    "coordinates": {"x": x, "y": y},
                    "message": f"点击输入框失败: {tap_result['message']}"
                }
            
            time.sleep(0.5)  # 增加等待时间确保获得焦点
            
            # 方法1: 使用多次退格删除（最可靠的方式）
            try:
                # 先移动到文本末尾（确保删除所有内容）
                for _ in range(5):  # 多次按下end键确保到达末尾
                    self.device.shell("input keyevent KEYCODE_MOVE_END")
                    time.sleep(0.02)
                
                # 执行删除操作
                delete_count = 0
                for i in range(200):  # 增加删除次数
                    self.device.shell("input keyevent KEYCODE_DEL")
                    delete_count += 1
                    # 控制删除速度，避免过快导致系统响应不及时
                    if i % 15 == 0:
                        time.sleep(0.1)
                    else:
                        time.sleep(0.02)
                
                # 删除完成后，再次点击确保焦点仍在输入框
                time.sleep(0.3)
                self.tap(x, y)
                time.sleep(0.3)
                
                return {
                    "success": True,
                    "action": "clear_input_field",
                    "coordinates": {"x": x, "y": y},
                    "method": "reliable_delete",
                    "delete_count": delete_count,
                    "message": f"已使用可靠删除方式清空输入框({x}, {y})，删除了{delete_count}次"
                }
                
            except Exception as e1:
                # 方法2: 备选方案 - 选择全部删除
                try:
                    # 三连击选择全部内容
                    for i in range(3):
                        self.tap(x, y)
                        time.sleep(0.15)
                    
                    time.sleep(0.3)
                    
                    # 删除选中内容
                    self.device.shell("input keyevent KEYCODE_DEL")
                    time.sleep(0.2)
                    
                    # 确保焦点还在输入框
                    self.tap(x, y)
                    time.sleep(0.3)
                    
                    return {
                        "success": True,
                        "action": "clear_input_field",
                        "coordinates": {"x": x, "y": y},
                        "method": "triple_tap_delete",
                        "message": f"已使用三连击删除方式清空输入框({x}, {y})"
                    }
                    
                except Exception as e2:
                    # 方法3: 最简单方案 - 直接删除
                    try:
                        # 简单的多次删除，删除完后重新点击
                        for i in range(100):
                            self.device.shell("input keyevent KEYCODE_DEL")
                            if i % 20 == 0:
                                time.sleep(0.1)
                        
                        # 重新获取焦点
                        time.sleep(0.5)
                        self.tap(x, y)
                        time.sleep(0.5)
                        
                        return {
                            "success": True,
                            "action": "clear_input_field",
                            "coordinates": {"x": x, "y": y},
                            "method": "simple_delete",
                            "message": f"已使用简单删除方式清空输入框({x}, {y})"
                        }
                        
                    except Exception as e3:
                        return {
                            "success": False,
                            "action": "clear_input_field",
                            "coordinates": {"x": x, "y": y},
                            "message": f"所有清空方法都失败了。错误: {str(e3)}"
                        }
        
        except Exception as e:
            return {
                "success": False,
                "action": "clear_input_field",
                "coordinates": {"x": x, "y": y},
                "message": f"清空输入框失败: {str(e)}"
            }

    def clear_input_and_type(self, x: int, y: int, text: str, use_dedicated_clear: bool = True) -> Dict[str, Any]:
        """
        MCP工具: 清空输入框并输入新文本
        
        Args:
            x (int): 输入框的X坐标
            y (int): 输入框的Y坐标
            text (str): 要输入的文本内容
            use_dedicated_clear (bool): 是否使用专用清空方法（推荐），默认True
            
        Returns:
            Dict[str, Any]: 包含操作结果和详细状态信息
        """
        try:
            if use_dedicated_clear:
                # 使用专用的清空方法（推荐方式）
                clear_result = self.clear_input_field(x, y)
                if not clear_result["success"]:
                    return {
                        "success": False,
                        "action": "clear_input_and_type",
                        "step": "clear",
                        "coordinates": {"x": x, "y": y},
                        "text": text,
                        "clear_result": clear_result,
                        "message": f"清空输入框失败: {clear_result['message']}"
                    }
                
                # 清空后再次确保获得焦点，等待足够时间
                time.sleep(0.5)
                
                # 再次点击输入框确保焦点正确
                refocus_result = self.tap(x, y)
                time.sleep(0.5)
                
                # 输入新文本
                input_result = self.input_text(text)
                if not input_result["success"]:
                    # 如果输入失败，尝试重新获取焦点后再试一次
                    time.sleep(0.3)
                    self.tap(x, y)
                    time.sleep(0.5)
                    input_result = self.input_text(text)
                    
                    if not input_result["success"]:
                        return {
                            "success": False,
                            "action": "clear_input_and_type", 
                            "step": "input",
                            "coordinates": {"x": x, "y": y},
                            "text": text,
                            "clear_result": clear_result,
                            "input_result": input_result,
                            "message": f"输入文本失败（重试后仍失败): {input_result['message']}"
                        }
                
                return {
                    "success": True,
                    "action": "clear_input_and_type",
                    "coordinates": {"x": x, "y": y},
                    "text": text,
                    "method": "dedicated_clear",
                    "clear_result": clear_result,
                    "refocus_result": refocus_result,
                    "input_result": input_result,
                    "message": f"已清空输入框({x}, {y})并输入新文本: {text}"
                }
                
            else:
                # 备选方式：简单的点击+多次删除+输入
                tap_result = self.tap(x, y)
                if not tap_result["success"]:
                    return {
                        "success": False,
                        "action": "clear_input_and_type",
                        "step": "tap",
                        "coordinates": {"x": x, "y": y},
                        "text": text,
                        "message": f"点击输入框失败: {tap_result['message']}"
                    }
                
                time.sleep(0.5)
                
                # 简单的清空方式：多次删除
                for i in range(100):
                    self.press_key(67)  # KEYCODE_DEL
                    if i % 20 == 0:
                        time.sleep(0.05)
                
                time.sleep(0.3)
                
                # 输入新文本
                input_result = self.input_text(text)
                if not input_result["success"]:
                    return {
                        "success": False,
                        "action": "clear_input_and_type",
                        "step": "input", 
                        "coordinates": {"x": x, "y": y},
                        "text": text,
                        "message": f"输入文本失败: {input_result['message']}"
                    }
                
                return {
                    "success": True,
                    "action": "clear_input_and_type",
                    "coordinates": {"x": x, "y": y},
                    "text": text,
                    "method": "simple_clear",
                    "tap_result": tap_result,
                    "input_result": input_result,
                    "message": f"已清空输入框({x}, {y})并输入新文本: {text}"
                }
            
        except Exception as e:
            return {
                "success": False,
                "action": "clear_input_and_type",
                "coordinates": {"x": x, "y": y},
                "text": text,
                "message": f"清空输入框并输入新文本失败: {str(e)}"
            }

    def replace_input_text(self, x: int, y: int, text: str) -> Dict[str, Any]:
        """
        MCP工具: 替换输入框文本（最可靠的方式）
        
        通过选中所有内容然后直接输入新文本来替换，避免复杂的清空逻辑
        
        Args:
            x (int): 输入框的X坐标
            y (int): 输入框的Y坐标
            text (str): 要输入的新文本内容
            
        Returns:
            Dict[str, Any]: 包含操作结果和状态信息
        """
        try:
            # 步骤1: 点击输入框获取焦点
            tap_result = self.tap(x, y)
            if not tap_result["success"]:
                return {
                    "success": False,
                    "action": "replace_input_text",
                    "step": "initial_tap",
                    "coordinates": {"x": x, "y": y},
                    "text": text,
                    "message": f"点击输入框失败: {tap_result['message']}"
                }
            
            time.sleep(0.5)
            
            # 步骤2: 三连击选择全部内容
            for i in range(3):
                self.tap(x, y)
                time.sleep(0.1)
            
            time.sleep(0.3)
            
            # 步骤3: 直接输入新文本（会自动替换选中的内容）
            input_result = self.input_text(text)
            
            if input_result["success"]:
                return {
                    "success": True,
                    "action": "replace_input_text",
                    "coordinates": {"x": x, "y": y},
                    "text": text,
                    "method": "triple_tap_replace",
                    "tap_result": tap_result,
                    "input_result": input_result,
                    "message": f"已成功替换输入框({x}, {y})的文本为: {text}"
                }
            else:
                # 如果直接输入失败，尝试备选方案
                return self._fallback_replace_input(x, y, text, tap_result)
                
        except Exception as e:
            return {
                "success": False,
                "action": "replace_input_text",
                "coordinates": {"x": x, "y": y},
                "text": text,
                "message": f"替换输入框文本失败: {str(e)}"
            }

    def _fallback_replace_input(self, x: int, y: int, text: str, initial_tap_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        备选的输入框文本替换方法
        """
        try:
            # 备选方案1: 先删除再输入
            time.sleep(0.5)
            
            # 重新点击获取焦点
            self.tap(x, y)
            time.sleep(0.5)
            
            # 执行一定数量的删除操作
            for i in range(80):
                self.device.shell("input keyevent KEYCODE_DEL")
                if i % 20 == 0:
                    time.sleep(0.1)
                else:
                    time.sleep(0.02)
            
            time.sleep(0.3)
            
            # 再次确保焦点在输入框
            self.tap(x, y)
            time.sleep(0.5)
            
            # 输入新文本
            input_result = self.input_text(text)
            
            return {
                "success": input_result["success"],
                "action": "replace_input_text",
                "coordinates": {"x": x, "y": y},
                "text": text,
                "method": "fallback_delete_input",
                "initial_tap_result": initial_tap_result,
                "input_result": input_result,
                "message": f"使用备选方案替换文本: {'成功' if input_result['success'] else '失败'}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "action": "replace_input_text",
                "coordinates": {"x": x, "y": y},
                "text": text,
                "method": "fallback_failed",
                "message": f"备选方案也失败了: {str(e)}"
            }

# MCP 工具函数映射表
MCP_TOOLS = {
    "get_screen_size": {
        "description": "获取Android设备屏幕分辨率",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "tap": {
        "description": "在屏幕指定坐标点击",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "X坐标"},
                "y": {"type": "integer", "description": "Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    "long_press": {
        "description": "在屏幕指定坐标长按",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "X坐标"},
                "y": {"type": "integer", "description": "Y坐标"},
                "duration": {"type": "integer", "description": "长按时长（毫秒）", "default": 1000}
            },
            "required": ["x", "y"]
        }
    },
    "swipe": {
        "description": "屏幕滑动操作",
        "parameters": {
            "type": "object",
            "properties": {
                "x1": {"type": "integer", "description": "起始X坐标"},
                "y1": {"type": "integer", "description": "起始Y坐标"},
                "x2": {"type": "integer", "description": "结束X坐标"},
                "y2": {"type": "integer", "description": "结束Y坐标"},
                "duration": {"type": "integer", "description": "滑动时长（毫秒）", "default": 500}
            },
            "required": ["x1", "y1", "x2", "y2"]
        }
    },
    "input_text": {
        "description": "输入指定文本",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "要输入的文本内容"}
            },
            "required": ["text"]
        }
    },
    "press_key": {
        "description": "模拟按键事件",
        "parameters": {
            "type": "object",
            "properties": {
                "keycode": {"type": "integer", "description": "Android KeyEvent 代码"}
            },
            "required": ["keycode"]
        }
    },
    "back": {
        "description": "模拟返回键",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "home": {
        "description": "模拟Home键",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "power": {
        "description": "模拟电源键",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "click_and_input": {
        "description": "点击输入框并输入字符（组合功能）",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "输入框的X坐标"},
                "y": {"type": "integer", "description": "输入框的Y坐标"},
                "text": {"type": "string", "description": "要输入的文本内容"},
                "delay": {"type": "number", "description": "点击后等待时间（秒）", "default": 0.5}
            },
            "required": ["x", "y", "text"]
        }
    },
    "clear_input_field": {
        "description": "清空输入框内容（专用方法，自动选择最佳清空策略）",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "输入框的X坐标"},
                "y": {"type": "integer", "description": "输入框的Y坐标"}
            },
            "required": ["x", "y"]
        }
    },
    "clear_input_and_type": {
        "description": "清空输入框并输入新文本",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "输入框的X坐标"},
                "y": {"type": "integer", "description": "输入框的Y坐标"},
                "text": {"type": "string", "description": "要输入的文本内容"},
                "use_dedicated_clear": {
                    "type": "boolean", 
                    "description": "是否使用专用清空方法（推荐），true为使用智能清空策略，false为使用简单删除方式", 
                    "default": True
                }
            },
            "required": ["x", "y", "text"]
        }
    },
    "replace_input_text": {
        "description": "替换输入框文本（最可靠的方式，推荐用于清空并输入新内容）",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "输入框的X坐标"},
                "y": {"type": "integer", "description": "输入框的Y坐标"},
                "text": {"type": "string", "description": "要输入的新文本内容"}
            },
            "required": ["x", "y", "text"]
        }
    }
}

# 示例用法
if __name__ == "__main__":
    # 初始化设备
    device = AndroidDevice()

    # 获取屏幕分辨率 (MCP模式)
    screen_info = device.get_screen_size()
    print(json.dumps(screen_info, indent=2, ensure_ascii=False))

    if screen_info["success"]:
        width, height = screen_info["width"], screen_info["height"]
        
        # 点击输入框并输入文字 (新功能)
        click_input_result = device.click_and_input(width // 2, 300, "Hello MCP World!")
        print(json.dumps(click_input_result, indent=2, ensure_ascii=False))
        
        time.sleep(2)
        
        # 方法1: 替换输入框文本（最推荐的方式）
        replace_result = device.replace_input_text(width // 2, 200, "新的文本内容 - 方法1")
        print("=== 替换输入框文本结果 ===")
        print(json.dumps(replace_result, indent=2, ensure_ascii=False))
        
        time.sleep(2)
        
        # 方法2: 专用清空输入框方法
        clear_result = device.clear_input_field(width // 2, 00)
        print("\n=== 清空输入框结果 ===")
        print(json.dumps(clear_result, indent=2, ensure_ascii=False))
        
        time.sleep(1)
        
        # 然后输入新文字
        input_result = device.input_text("清空后输入的新文字")
        print("\n=== 清空后输入结果 ===")
        print(json.dumps(input_result, indent=2, ensure_ascii=False))
        
        time.sleep(2)
        
        # 方法3: 清空输入框并输入新文字（使用智能清空策略）
        clear_input_result = device.clear_input_and_type(width // 2, 100, "新的文本内容 - 方法3", use_dedicated_clear=True)
        print("\n=== 清空并输入结果 ===")
        print(json.dumps(clear_input_result, indent=2, ensure_ascii=False))

    # 输出MCP工具定义
    print("\n=== MCP 工具定义 ===")
    print(json.dumps(MCP_TOOLS, indent=2, ensure_ascii=False))