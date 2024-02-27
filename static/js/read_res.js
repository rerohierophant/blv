// 获取要监测的元素
const targetNode = document.getElementById('response');

// 创建一个观察者实例并传入回调函数
const observer = new MutationObserver(function(mutationsList, observer) {
    for(let mutation of mutationsList) {
        if (mutation.type === 'childList' || mutation.type === 'characterData') {
            const newText = targetNode.textContent || targetNode.innerText;
            // 调用朗读函数
            speakText(newText);
        }
    }
});

// 使用配置项开始观察目标节点
observer.observe(targetNode, { childList: true, subtree: true, characterData: true });

// 定义一个朗读文本的函数
function speakText(text) {
    const synth = window.speechSynthesis;
    const utterThis = new SpeechSynthesisUtterance(text);
    synth.speak(utterThis);
}

document.getElementById('read-btn').addEventListener('click', function() {
    var text = document.getElementById('response').innerText;
    var speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
});