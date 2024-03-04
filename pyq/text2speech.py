import azure.cognitiveservices.speech as speechsdk
import time


def text2speech(text):
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = "a4796e6a8a6849f08536af545791b7ab"
    service_region = "eastus"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoqiuNeural"

    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.speak_text_async(text).get()
    # 获取当前时间戳
    timestamp = str(time.time())
    timestamp = timestamp.replace(".", "")
    stream = speechsdk.AudioDataStream(result)
    fp = f"static/audio/{timestamp}.mp3"
    stream.save_to_wav_file(fp)  # mp3文件保存路径
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return f"/{fp}"

