import streamlit as st
st.title('두근두근 다죽어월드 호텔 이벤트 응모')
a=st.text_input('이름을 입력해주세요')
b=st.selectbox('사용하는 계좌 은행을 선택해주세요',['토스','우리은행','카카오뱅크','IBK'])
if st.button('응모 결과'):
  st.write(a+'님! 그대는 해킹 당햇스ㅅㅂ니다ㅜㅜ!')
  st.info('이리 둔하실 수가')
  st.warning(b+' 1조 앙 ㄱㅁㄸ!!')
  st.error('gg ㅋ ㅋ ㅋ ㅋ ㅋ ㅋ ㅋ ㅋ ㅋ ㅋ ㅋ ㅋㅋ ㅋ ㅋ ㅋ ㅋ ')
  st.ballons()
