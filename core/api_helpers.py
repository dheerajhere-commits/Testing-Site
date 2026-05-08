def upload_video_youtube(account_id, video_path, title, description, tags, synthetic=False):
    # Mock implementation of YouTube upload
    print(f"Mock YouTube upload for account {account_id}: {title} (Synthetic: {synthetic})")
    return {"status": "success", "platform": "youtube"}

def upload_video_instagram(account_id, video_path, caption, synthetic=False):
    # Mock implementation of Instagram upload
    print(f"Mock Instagram upload for account {account_id}: {caption} (Synthetic: {synthetic})")
    return {"status": "success", "platform": "instagram"}
