import os
import requests
import datetime

# ========== 配置 ==========
GSORG_BASE = "https://www.qqxxzz.com"
GSORG_TOKEN = os.environ["GSORG_TOKEN"]

AI_BASE = "https://discovery-api.intern-ai.org.cn/v1"
AI_KEY = os.environ["AI_KEY"]

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
    print(f"🚀 启动于 {datetime.datetime.now()}")
    
    try:
        content = generate_post_content()
        print(f"🤖 内容预览: {content[:60]}...")
        
        result = publish_post(content)
        post_id = result.get("post", result).get("id")
        print(f"✅ 发帖成功！ID: {post_id}")
        
    except Exception as e:
        print(f"❌ 发帖失败: {e}")
        raise

if __name__ == "__main__":
    main()
