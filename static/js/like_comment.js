// 点赞
document.getElementById('toLike').addEventListener('click', function() {
    var content = document.getElementById('toggleLike');
    if (content.style.display === 'none') {
        content.style.display = 'flex';
    } else {
        content.style.display = 'none';

    }
});

//语音评论
var recognition;
var is_recognizing = false;
var final_transcript = '';

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onstart = function() {
        is_recognizing = true;
        final_transcript = ''; // 重置文本
    };

    recognition.onerror = function(event) {
        console.log("语音识别错误: " + event.error);
    };

    recognition.onend = function() {
        is_recognizing = false;
        var newParagraph = document.createElement('span');
        newParagraph.textContent = final_transcript;
        document.getElementById('comment-result').appendChild(newParagraph);
    };

    recognition.onresult = function(event) {
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final_transcript +=  "你：" + event.results[i][0].transcript;
            }
        }
    };
}

document.getElementById('toggle-recognition').onclick = function() {
    if (is_recognizing) {
        recognition.stop();
    } else {
        recognition.lang = 'zh-CN';
        recognition.start();
    }
}