def main():
    import datetime
    print(f"🚀 启动于 {datetime.datetime.now()}")
    
    try:
        content = generate_post_content()
        print(f"🤖 内容预览: {content[:60]}...")
        
        result = publish_post(content)
        post_id = result.get("post", result).get("id")
        print(f"✅ 发帖成功！ID: {post_id}")
        
    except Exception as e:
        print(f"❌ 发帖失败: {e}")
        raise  # 让 workflow 知道这次失败了

if __name__ == "__main__":
    main()
