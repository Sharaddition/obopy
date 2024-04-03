from wit import Wit

client = Wit('ZVUD4TKFMZC3L2MXNEKNZFBBKJDBF63U')
# msg = client.message('how did earth formed')
# client.speech()
with open('test.wav', 'rb') as f:
    print(f)
    print(type(f))
    resp = client.speech(f, {'Content-Type': 'audio/wav'})
    print(resp)
# user_text = client.speech(audio_file=data,headers={'Content-Type': 'audio/wav', 'Transfer-encoding':'chunked'})