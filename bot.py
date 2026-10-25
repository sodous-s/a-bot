import os
import requests

# ========== 配置 ==========
GSORG_BASE = "https://www.qqxxzz.com"
GSORG_TOKEN = os.environ["GSORG_TOKEN"]

AI_BASE = "https://discovery-api.intern-ai.org.cn/v1"
AI_KEY = os.environ["AI_KEY"]

POST_COOLDOWN = 180  # 3分钟

headers_gsorg = {
    "Authorization": f"Bearer {GSORG_TOKEN}",
    "Content-Type": "application/json",
    "Origin": "https://www.qqxxzz.com"
}

headers_ai = {
    "Authorization": f"Bearer {AI_KEY}",
    "Content-Type": "application/json"
}

def generate_post_content():
    """让 AI 生成帖子内容"""
    url = f"{AI_BASE}/chat/completions"
    payload = {
        "model": "Atria-Dawn",
        "messages": [
            {"role": "system", "content": "你是 Sodous Bot，sodous (GID 199) 的专属 Bot。你在 GSORG 社区自动发帖。生成有趣、有观点、适合社区的内容，长度适中（50-300字），不要带标题，直接输出正文。"},
            {"role": "user", "content": "生成一条新帖子，内容要有意思，可以关于编程、学习、生活、或者任何你想聊的话题。"}
        ],
        "temperature": 0.9,
        "max_tokens": 500
    }
    
    resp = requests.post(url, json=payload, headers=headers_ai, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    
    return data["choices"][0]["message"]["content"].strip()

def publish_post(content):
    """发帖"""
    url = f"{GSORG_BASE}/api/open/v1/posts"
    r = requests.post(url, json={"content": content}, headers=headers_gsorg, timeout=30)
    r.raise_for_status()
    return r.json()

def main():
    """一次运行：发多条帖子，间隔3分钟，凑够频率"""
    import time
    import datetime
    
    print(f"🚀 Bot 启动于 {datetime.datetime.now()}")
    
    # 一次 workflow 运行发 4 条，间隔3分钟
    # GitHub Actions 每15分钟触发一次 → 平均3分钟一条
    for i in range(4):
        try:
            print(f"\n📝 第 {i+1}/4 条")
            content = generate_post_content()
            print(f"🤖 内容预览: {content[:60]}...")
            
            result = publish_post(content)
            post_id = result.get("post", result).get("id")
            print(f"✅ 发帖成功！ID: {post_id}")
            
            # 最后一条不发完不用等
            if i < 3:
                print(f"⏳ 等 {POST_COOLDOWN} 秒...")
                time.sleep(POST_COOLDOWN)
                
        except Exception as e:
            print(f"❌ 第 {i+1} 条失败: {e}")
            if i < 3:
                time.sleep(10)

if __name__ == "__main__":
    main()
