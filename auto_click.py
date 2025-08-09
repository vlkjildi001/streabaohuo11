from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import os

# 设置无头浏览器参数
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

log_file = "click_log.txt"
log_retention_days = 2  # 保留天数

def clean_old_logs():
    if not os.path.exists(log_file):
        return
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        cutoff = datetime.now() - timedelta(days=log_retention_days)
        cleaned_lines = []
        for line in lines:
            if line.startswith("["):
                try:
                    timestamp_str = line.split("]")[0][1:]
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    if timestamp >= cutoff:
                        cleaned_lines.append(line)
                except:
                    cleaned_lines.append(line)
            else:
                cleaned_lines.append(line)
        with open(log_file, "w", encoding="utf-8") as f:
            f.writelines(cleaned_lines)
    except Exception as e:
        print(f"日志清理失败：{e}")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    print(entry.strip())
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

clean_old_logs()

try:
    driver.get("https://11str25n0809.streamlit.app/")
    
    wait = WebDriverWait(driver, 50)  # 最多等50秒
    try:
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., '启动部署')]"))
        )
        button.click()
        log("按钮已点击")
    except Exception as e:
        log(f"未发现按钮或点击失败: {e}")

except Exception as e:
    log(f"脚本异常出错: {e}")

finally:
    driver.quit()
