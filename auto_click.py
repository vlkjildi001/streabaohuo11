from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time
import os

# 日志文件路径和保留天数
log_file = "click_log.txt"
log_retention_days = 2

# 清理旧日志
def clean_old_logs():
    if not os.path.exists(log_file):
        return

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        cleaned_lines = []
        cutoff = datetime.now() - timedelta(days=log_retention_days)

        for line in lines:
            if line.startswith("["):
                try:
                    timestamp_str = line.split("]")[0][1:]
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    if timestamp >= cutoff:
                        cleaned_lines.append(line)
                except:
                    cleaned_lines.append(line)  # 非时间行保留
            else:
                cleaned_lines.append(line)

        with open(log_file, "w", encoding="utf-8") as f:
            f.writelines(cleaned_lines)

    except Exception as e:
        print(f"日志清理失败：{e}")

# 设置无头浏览器参数
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    clean_old_logs()

    driver.get("https://app-8w4wwungk5qvcotqhlsvgr.streamlit.app/")
    
    wait = WebDriverWait(driver, 30)
    try:
        # 显式等待“启动部署”按钮可点击
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '启动部署')]")))
        button.click()
        log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 按钮已点击\n"
        print("检测到按钮，已点击。")
    except Exception as e:
        log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 未发现按钮或点击失败: {e}\n"
        print(f"未检测到按钮或点击失败: {e}")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

except Exception as e:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] 脚本运行错误：{str(e)}\n")
    print(f"脚本运行错误：{e}")

finally:
    driver.quit()
