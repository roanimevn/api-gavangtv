import requests
import re
import json

def crawl_m3u8():
    url = "https://gavangtvx.com/" 
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://gavangtvx.com/"
    }
    
    print(f"Đang bắt đầu quét link từ: {url}")
    
    unique_links = []
    status_msg = "Success"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Mã phản hồi từ server: {response.status_code}")
        
        if response.status_code == 200:
            html_content = response.text
            # Dùng Regex tìm các link .m3u8
            m3u8_pattern = r'https?://[^\s<>"]+?\.m3u8[^\s<>"]*'
            links = re.findall(m3u8_pattern, html_content)
            unique_links = list(set(links))
            print(f"Tìm thấy {len(unique_links)} link m3u8.")
        else:
            status_msg = f"HTTP Error {response.status_code}"
            print(status_msg)
            
    except Exception as e:
        status_msg = f"Exception: {str(e)}"
        print(f"Lỗi trong quá trình cào dữ liệu: {e}")
        
    # LUÔN LUÔN tạo file links.json (dù thành công hay lỗi) để GitHub luôn có file push lên
    result_data = {
        "target_url": url,
        "status": status_msg,
        "total_found": len(unique_links),
        "m3u8_links": unique_links
    }
    
    with open("links.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)
    print("Đã ghi file links.json thành công!")

if __name__ == "__main__":
    crawl_m3u8()

