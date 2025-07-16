// 引入 Auto.js 6 模块
auto(); // 初始化 Auto.js
device.wakeUp(); // 唤醒屏幕
sleep(3000);

console.log("开始执行美团外卖脚本...");
console.log("设备信息：", device.width + "x" + device.height);

// ================== 通用按钮查找和点击函数 ==================

/**
 * 通用元素查找函数
 * @param {Object} options 查找选项
 * @param {Array<string>} options.texts 要查找的文本数组
 * @param {Array<string>} options.descs 要查找的描述数组  
 * @param {Array<string>} options.ids 要查找的ID数组
 * @param {string} options.className 要查找的类名
 * @param {Array<Array<number>>} options.coordinates 备用坐标数组 [[x,y], [x,y]]
 * @param {number} options.timeout 查找超时时间(毫秒)
 * @param {string} options.name 元素名称(用于日志)
 * @returns {Object|null} 找到的元素或null
 */
function findElement(options) {
    const {
        texts = [],
        descs = [],
        ids = [],
        className = "",
        coordinates = [],
        timeout = 1000,
        name = "元素"
    } = options;
    
    console.log(`正在查找${name}...`);
        
    if (ids.length > 0) {
        console.log(`方法1：通过ID查找${name}`);
        for (let i = 0; i < ids.length; i++) {
            let element = id(ids[i]).findOne(timeout);
            if (element) {
                console.log(`找到${name} - ID方式: "${ids[i]}"`);
                return element;
            }
        }
    }
    
    // 方法2：通过描述查找
    if (descs.length > 0) {
        console.log(`方法2：通过描述查找${name}`);
        for (let i = 0; i < descs.length; i++) {
            let element = desc(descs[i]).findOne(timeout);
            if (element) {
                console.log(`找到${name} - 描述方式: "${descs[i]}"`);
                return element;
            }
        }
    }

    console.log(`所有选择器方法都未找到${name}`);
    return null;
}

/**
 * 通用点击函数
 * @param {Object} element 要点击的元素
 * @param {Object} options 点击选项
 * @param {Array<Array<number>>} options.backupCoordinates 备用坐标数组
 * @param {string} options.successText 成功验证文本
 * @param {string} options.name 元素名称
 * @param {number} options.waitTime 点击后等待时间
 * @returns {boolean} 是否点击成功
 */
function clickElement(element, options = {}) {
    const {
        backupCoordinates = [],
        successText = "",
        name = "元素",
        waitTime = 1000
    } = options;
    
    if (element) {
        console.log(`找到${name}，正在点击...`);
        console.log(`${name}信息:`, element.toString());
        
        try {
            element.click();
            sleep(waitTime);
        
            console.log(`${name}点击完成`);
            return true;
            
        } catch (error) {
            console.log(`点击${name}时发生错误:`, error);
        }
    } else {
        console.log(`未找到${name}...`);
    }
}

/**
 * 文本输入函数
 * @param {Object} options 输入选项
 * @param {Array<string>} options.texts 搜索框的可能文本
 * @param {Array<string>} options.descs 搜索框的可能描述
 * @param {Array<string>} options.ids 搜索框的可能ID
 * @param {string} options.inputText 要输入的文本
 * @param {Array<Array<number>>} options.backupCoordinates 备用坐标
 * @param {string} options.name 输入框名称
 * @param {boolean} options.pressEnter 是否按回车键提交
 * @returns {boolean} 是否输入成功
 */
function inputText(options) {
    const {
        texts = [],
        descs = [],
        ids = [],
        inputText = "",
        backupCoordinates = [],
        name = "输入框",
        pressEnter = true
    } = options;
    
    // 查找输入框
    let inputBox = findElement({
        texts,
        descs,
        ids,
        className: "android.widget.EditText",
        name
    });
    
    if (inputBox) {
        console.log(`找到${name}，开始输入文本...`);
        
        try {
            // 点击输入框
            inputBox.click();
            sleep(1000);
            
            // 清空并输入文本
            inputBox.setText("");
            sleep(500);
            inputBox.setText(inputText);
            sleep(1000);
            
            console.log(`已输入文本: "${inputText}"`);
            
            // 提交输入
            if (pressEnter) {
                // 尝试查找搜索按钮
                let submitBtn = text("搜索").findOne(2000) || text("确认").findOne(2000);
                if (submitBtn) {
                    console.log("找到提交按钮，点击提交");
                    submitBtn.click();
                } else {
                    console.log("未找到提交按钮，按回车键提交");
                    KeyCode("KEYCODE_ENTER");
                }
            }
            
            return true;
            
        } catch (error) {
            console.log(`输入文本时发生错误:`, error);
            return inputByCoordinates(backupCoordinates, inputText, name, pressEnter);
        }
        
    } else {
        console.log(`未找到${name}，尝试坐标输入...`);
        return inputByCoordinates(backupCoordinates, inputText, name, pressEnter);
    }
}

/**
 * 坐标输入函数
 * @param {Array<Array<number>>} coordinates 坐标数组
 * @param {string} inputText 要输入的文本
 * @param {string} name 输入框名称
 * @param {boolean} pressEnter 是否按回车
 * @returns {boolean} 是否成功
 */
function inputByCoordinates(coordinates, inputText, name = "输入框", pressEnter = true) {
    if (coordinates.length === 0) {
        console.log(`没有备用坐标，无法输入到${name}`);
        return false;
    }
    
    console.log(`通过坐标输入到${name}`);
    
    for (let i = 0; i < coordinates.length; i++) {
        let [x, y] = coordinates[i];
        console.log(`尝试点击输入框坐标: (${x}, ${y})`);
        click(x, y);
        sleep(1000);
        
        // 检查是否成功激活了输入框
        if (className("android.widget.EditText").exists()) {
            console.log("成功激活输入框，开始输入");
            setText(inputText);
            sleep(1000);
            
            if (pressEnter) {
                KeyCode("KEYCODE_ENTER");
            }
            
            return true;
        }
    }
    
    console.log(`所有坐标都未能成功激活${name}`);
    return false;
}

/**
 * 获取元素详细信息
 * @param {Object} element 要分析的元素
 * @param {number} index 元素索引
 * @returns {Object} 元素信息对象
 */
function getElementInfo(element, index) {
    try {
        const bounds = element.bounds();
        const info = {
            index: index,
            text: element.text() || "",
            desc: element.desc() || "",
            id: element.id() || "",
            className: element.className() || "",
            clickable: element.clickable() || false,
            checkable: element.checkable() || false,
            checked: element.checked() || false,
            scrollable: element.scrollable() || false,
            editable: element.editable() || false,
            enabled: element.enabled() || false,
            focusable: element.focusable() || false,
            focused: element.focused() || false,
            selected: element.selected() || false,
            longClickable: element.longClickable() || false,
            bounds: bounds ? {
                left: bounds.left,
                top: bounds.top,
                right: bounds.right,
                bottom: bounds.bottom,
                width: bounds.width(),
                height: bounds.height(),
                centerX: bounds.centerX(),
                centerY: bounds.centerY()
            } : null,
            depth: element.depth() || 0,
            packageName: element.packageName() || "",
            visibleToUser: element.visibleToUser() || false
        };
        
        // 添加特殊属性
        try {
            if (element.className() === "android.widget.EditText") {
                info.hint = element.hint() || "";
                info.inputType = element.inputType() || "";
            }
            
            if (element.className() === "android.widget.TextView" || element.className() === "android.widget.EditText") {
                info.textSize = element.textSize() || 0;
                info.textColor = element.textColor() || "";
            }
            
            if (element.className() === "android.widget.ImageView") {
                info.drawable = element.drawable() || null;
            }
            
            if (element.className() === "android.widget.ListView" || element.className() === "android.widget.RecyclerView") {
                info.childCount = element.childCount() || 0;
            }
            
        } catch (e) {
            // 忽略获取特殊属性时的错误
        }
        
        return info;
        
    } catch (error) {
        console.log(`获取元素信息时出错:`, error.message);
        return {
            index: index,
            error: error.message,
            element: element.toString()
        };
    }
}

/**
 * 输出元素信息
 * @param {Object} elementInfo 元素信息对象
 * @param {boolean} detailed 是否输出详细信息
 */
function printElementInfo(elementInfo, detailed = false) {
    if (elementInfo.error) {
        console.log(`元素 ${elementInfo.index}: [错误] ${elementInfo.error}`);
        return;
    }
    
    const displayText = elementInfo.text || elementInfo.desc || elementInfo.id || elementInfo.className;
    console.log(`元素 ${elementInfo.index}: ${displayText}`);
    
    if (detailed) {
        console.log(`  文本: "${elementInfo.text}"`);
        console.log(`  描述: "${elementInfo.desc}"`);
        console.log(`  ID: "${elementInfo.id}"`);
        // console.log(`  类名: ${elementInfo.className}`);
        // console.log(`  包名: ${elementInfo.packageName}`);
        // console.log(`  可点击: ${elementInfo.clickable}`);
        // console.log(`  可编辑: ${elementInfo.editable}`);
        // console.log(`  可滚动: ${elementInfo.scrollable}`);
        // console.log(`  可长按: ${elementInfo.longClickable}`);
        // console.log(`  可勾选: ${elementInfo.checkable}`);
        // console.log(`  已勾选: ${elementInfo.checked}`);
        // console.log(`  已选中: ${elementInfo.selected}`);
        // console.log(`  已获焦: ${elementInfo.focused}`);
        // console.log(`  可获焦: ${elementInfo.focusable}`);
        // console.log(`  已启用: ${elementInfo.enabled}`);
        // console.log(`  用户可见: ${elementInfo.visibleToUser}`);
        // console.log(`  层级深度: ${elementInfo.depth}`);
        
        if (elementInfo.bounds) {
            console.log(`  位置: (${elementInfo.bounds.left},${elementInfo.bounds.top})-(${elementInfo.bounds.right},${elementInfo.bounds.bottom})`);
            console.log(`  尺寸: ${elementInfo.bounds.width}x${elementInfo.bounds.height}`);
            console.log(`  中心: (${elementInfo.bounds.centerX},${elementInfo.bounds.centerY})`);
        }
        
        // 输出特殊属性
        if (elementInfo.hint) {
            console.log(`  提示文本: "${elementInfo.hint}"`);
        }
        if (elementInfo.inputType) {
            console.log(`  输入类型: ${elementInfo.inputType}`);
        }
        if (elementInfo.textSize) {
            console.log(`  文本大小: ${elementInfo.textSize}`);
        }
        if (elementInfo.textColor) {
            console.log(`  文本颜色: ${elementInfo.textColor}`);
        }
        if (elementInfo.childCount !== undefined) {
            console.log(`  子元素数量: ${elementInfo.childCount}`);
        }
        
        console.log("  ---");
    }
}

/**
 * 全面分析页面所有可交互元素
 * @param {Object} options 分析选项
 * @param {boolean} options.detailed 是否输出详细信息
 * @param {boolean} options.includeNonClickable 是否包含不可点击元素
 * @param {number} options.maxElements 最大分析元素数量
 * @param {boolean} options.exportToFile 是否导出到文件
 * @param {Array<string>} options.focusClasses 重点关注的类名
 * @returns {Array} 所有元素信息数组
 */
function analyzeAllInteractiveElements(options = {}) {
    const {
        detailed = false,
        includeNonClickable = true,
        maxElements = 500,
        exportToFile = false,
        focusClasses = [
            "android.widget.Button",
            "android.widget.TextView",
            "android.widget.EditText",
            "android.widget.ImageView",
            "android.widget.ImageButton",
            "android.widget.CheckBox",
            "android.widget.RadioButton",
            "android.widget.Switch",
            "android.widget.SeekBar",
            "android.widget.Spinner",
            "android.widget.ListView",
            "android.widget.RecyclerView",
            "android.widget.ScrollView",
            "android.widget.ViewPager",
            "android.widget.TabHost",
            "android.widget.ToggleButton",
            "android.view.ViewGroup",
            "android.widget.LinearLayout",
            "android.widget.RelativeLayout",
            "android.widget.FrameLayout",
            "android.widget.ConstraintLayout"
        ]
    } = options;
    
    console.log("========== 全面页面交互元素分析 ==========");
    console.log(`设备信息: ${device.width}x${device.height}`);
    console.log(`分析选项: 详细=${detailed}, 包含不可点击=${includeNonClickable}, 最大元素=${maxElements}`);
    console.log("==========================================");
    
    const allElementsInfo = [];
    
    try {
        // 1. 获取所有可点击元素
        console.log("1. 分析可点击元素...");
        let clickableElements = clickable(true).find();
        console.log(`找到可点击元素: ${clickableElements.length} 个`);
        
        // 2. 获取所有可编辑元素
        console.log("2. 分析可编辑元素...");
        let editableElements = editable(true).find();
        console.log(`找到可编辑元素: ${editableElements.length} 个`);
        
        // 3. 获取所有可滚动元素
        console.log("3. 分析可滚动元素...");
        let scrollableElements = scrollable(true).find();
        console.log(`找到可滚动元素: ${scrollableElements.length} 个`);
        
        // 4. 获取所有可长按元素
        console.log("4. 分析可长按元素...");
        let longClickableElements = longClickable(true).find();
        console.log(`找到可长按元素: ${longClickableElements.length} 个`);
        
        // 5. 获取所有可勾选元素
        console.log("5. 分析可勾选元素...");
        let checkableElements = checkable(true).find();
        console.log(`找到可勾选元素: ${checkableElements.length} 个`);
        
        // 6. 按类名获取特定类型元素
        console.log("6. 按类名分析特定元素...");
        let elementsByClass = {};
        
        focusClasses.forEach(clsName => {
            try {
                let elements = className(clsName).find();
                if (elements.length > 0) {
                    elementsByClass[clsName] = elements;
                    console.log(`  ${clsName}: ${elements.length} 个`);
                }
            } catch (e) {
                console.log(`  获取 ${clsName} 时出错: ${e.message}`);
            }
        });
        
        // 7. 合并所有元素并去重
        console.log("7. 合并和去重元素...");
        let allElements = new Set();
        
        // 添加各种类型的元素
        [clickableElements, editableElements, scrollableElements, longClickableElements, checkableElements].forEach(elements => {
            elements.forEach(element => {
                allElements.add(element);
            });
        });
        
        // 添加按类名找到的元素
        Object.values(elementsByClass).forEach(elements => {
            elements.forEach(element => {
                allElements.add(element);
            });
        });
        
        // 如果包含不可点击元素，添加所有可见元素
        if (includeNonClickable) {
            console.log("8. 添加其他可见元素...");
            try {
                let allVisibleElements = visibleToUser(true).find();
                console.log(`找到可见元素: ${allVisibleElements.length} 个`);
                allVisibleElements.forEach(element => {
                    allElements.add(element);
                });
            } catch (e) {
                console.log(`获取可见元素时出错: ${e.message}`);
            }
        }
        
        // 转换为数组并限制数量
        let elementsArray = Array.from(allElements).slice(0, maxElements);
        console.log(`最终分析元素总数: ${elementsArray.length} 个`);
        
        // 8. 分析每个元素
        console.log("9. 详细分析每个元素...");
        console.log("==========================================");
        
        elementsArray.forEach((element, index) => {
            const elementInfo = getElementInfo(element, index + 1);
            allElementsInfo.push(elementInfo);
            
            // 只显示有意义的元素
            if (elementInfo.text || elementInfo.desc || elementInfo.id || elementInfo.clickable || elementInfo.editable || elementInfo.scrollable) {
                printElementInfo(elementInfo, detailed);
            }
        });
        
        // 9. 统计分析
        console.log("==========================================");
        console.log("统计信息:");
        console.log(`总元素数量: ${allElementsInfo.length}`);
        console.log(`可点击元素: ${allElementsInfo.filter(e => e.clickable).length}`);
        console.log(`可编辑元素: ${allElementsInfo.filter(e => e.editable).length}`);
        console.log(`可滚动元素: ${allElementsInfo.filter(e => e.scrollable).length}`);
        console.log(`可长按元素: ${allElementsInfo.filter(e => e.longClickable).length}`);
        console.log(`可勾选元素: ${allElementsInfo.filter(e => e.checkable).length}`);
        console.log(`有文本元素: ${allElementsInfo.filter(e => e.text).length}`);
        console.log(`有描述元素: ${allElementsInfo.filter(e => e.desc).length}`);
        console.log(`有ID元素: ${allElementsInfo.filter(e => e.id).length}`);
        
        // 10. 按类名分组统计
        console.log("按类名统计:");
        let classStats = {};
        allElementsInfo.forEach(info => {
            if (info.className) {
                classStats[info.className] = (classStats[info.className] || 0) + 1;
            }
        });
        
        Object.entries(classStats).sort((a, b) => b[1] - a[1]).forEach(([className, count]) => {
            console.log(`  ${className}: ${count} 个`);
        });
        
        // 11. 导出到文件（如果需要）
        if (exportToFile) {
            console.log("11. 导出元素信息到文件...");
            try {
                const exportData = {
                    timestamp: new Date().toISOString(),
                    deviceInfo: {
                        width: device.width,
                        height: device.height
                    },
                    summary: {
                        totalElements: allElementsInfo.length,
                        clickableElements: allElementsInfo.filter(e => e.clickable).length,
                        editableElements: allElementsInfo.filter(e => e.editable).length,
                        scrollableElements: allElementsInfo.filter(e => e.scrollable).length
                    },
                    elements: allElementsInfo
                };
                
                const fileName = `/sdcard/ui_elements_${Date.now()}.json`;
                files.write(fileName, JSON.stringify(exportData, null, 2));
                console.log(`元素信息已导出到: ${fileName}`);
            } catch (e) {
                console.log(`导出文件时出错: ${e.message}`);
            }
        }
        
        console.log("========== 分析完成 ==========");
        
        return allElementsInfo;
        
    } catch (error) {
        console.log("分析页面元素时发生错误:", error);
        return allElementsInfo;
    }
}

// 保持原有的函数名以便向后兼容
function analyzeClickableElements() {
    return analyzeAllInteractiveElements({
        detailed: false,
        includeNonClickable: false,
        maxElements: 200
    });
}

/**
 * 查找特定类型的元素
 * @param {string} elementType 元素类型 (button, input, image, list, etc.)
 * @param {Object} options 查找选项
 * @returns {Array} 找到的元素信息数组
 */
function findElementsByType(elementType, options = {}) {
    const typeMapping = {
        'button': ['android.widget.Button', 'android.widget.ImageButton'],
        'input': ['android.widget.EditText'],
        'text': ['android.widget.TextView'],
        'image': ['android.widget.ImageView'],
        'list': ['android.widget.ListView', 'android.widget.RecyclerView'],
        'scroll': ['android.widget.ScrollView'],
        'checkbox': ['android.widget.CheckBox'],
        'radio': ['android.widget.RadioButton'],
        'switch': ['android.widget.Switch'],
        'seekbar': ['android.widget.SeekBar'],
        'spinner': ['android.widget.Spinner'],
        'layout': ['android.widget.LinearLayout', 'android.widget.RelativeLayout', 'android.widget.FrameLayout']
    };
    
    const classNames = typeMapping[elementType.toLowerCase()];
    if (!classNames) {
        console.log(`未知的元素类型: ${elementType}`);
        return [];
    }
    
    console.log(`正在查找 ${elementType} 类型的元素...`);
    
    let foundElements = [];
    classNames.forEach(clsName => {
        try {
            let elements = className(clsName).find();
            elements.forEach((element, index) => {
                const elementInfo = getElementInfo(element, foundElements.length + 1);
                foundElements.push(elementInfo);
            });
        } catch (e) {
            console.log(`查找 ${clsName} 时出错: ${e.message}`);
        }
    });
    
    console.log(`找到 ${foundElements.length} 个 ${elementType} 元素`);
    return foundElements;
}

/**
 * 查找并点击元素的组合函数
 * @param {Object} findOptions 查找选项
 * @param {Object} clickOptions 点击选项
 * @returns {boolean} 是否成功
 */
function findAndClick(findOptions, clickOptions = {}) {
    const element = findElement(findOptions);
    return clickElement(element, clickOptions);
}

// 1. 打开美团 App
console.log("正在打开美团App...");
launchApp("美团");
sleep(1000); // 等待App启动

// 使用新的全面分析功能
analyzeAllInteractiveElements({
    detailed: true,
    includeNonClickable: true,
    maxElements: 300,
    exportToFile: true
});

// 2. 使用公共函数查找并点击外卖按钮
console.log("正在查找外卖按钮...");

let screenWidth = device.width;
let screenHeight = device.height;

// 定义外卖按钮的查找参数
let waimaiOptions = {
    texts: ["外卖"],
    descs: ["外卖"],
    ids: [
        "com.sankuai.meituan:id/waimai_channel_icon",
    ],
    name: "外卖按钮"
};

// findAndClick(waimaiOptions)

console.log("脚本执行完成");