from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# دالة لتحميل الأغاني من YouTube أو أي منصة مشابهة
def download_song(song_name, format_choice):
    ydl_opts = {
        'format': 'bestaudio/best' if format_choice == 'mp3' else 'bestvideo+bestaudio/best',
        'outtmpl': f'./downloads/{song_name}.%(ext)s',  # حفظ الأغنية في مجلد downloads
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{song_name}", download=True)
        # احصل على اسم الأغنية والفيديو
        title = info_dict.get('title', None)
        url = info_dict.get('url', None)
        return title, url

@app.route('/play', methods=['GET'])
def play_song():
    song_name = request.args.get('song')
    if not song_name:
        return jsonify({'error': 'Please provide a song name'}), 400

    # عرض خيارات للمستخدم
    song_title, song_url = download_song(song_name, format_choice='mp3')

    # عرض معلومات الأغنية للمستخدم
    response = {
        'song_title': song_title,
        'song_url': song_url,
        'message': 'Please select a format: mp3 or video.'
    }

    return jsonify(response)


@app.route('/download', methods=['GET'])
def download():
    song_name = request.args.get('song')
    format_choice = request.args.get('format')
    
    if not song_name or not format_choice:
        return jsonify({'error': 'Please provide song name and format (mp3 or video).'}), 400

    # تنزيل الأغنية بناءً على الاختيار
    song_title, song_url = download_song(song_name, format_choice)

    # إرسال رابط التنزيل للمستخدم
    return jsonify({
        'message': f"Song '{song_title}' downloaded successfully.",
        'download_link': f"./downloads/{song_title}.mp3" if format_choice == 'mp3' else f"./downloads/{song_title}.mp4"
    })


if __name__ == '__main__':
    app.run(debug=True)

