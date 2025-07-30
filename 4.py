import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.title('수준별 물리 실험 그래프 그리기')

level = st.slider("난이도", 1, 3, 2)

if level == 1:
    st.header('원하는 실험을 선택하세요.')
    exp = st.radio("실험 선택", ['등가속도 운동', '단진자운동'])

    if exp == '등가속도 운동':
        st.title("등가속도 운동 시뮬레이터")

        x0 = st.slider("초기 위치 (x₀)", -50.0, 50.0, 0.0)
        v0 = st.slider("초기 속도 (v₀, m/s)", -20.0, 20.0, 0.0)
        a = st.slider("가속도 (a, m/s²)", -10.0, 10.0, 0.0)
        t_max = st.slider("시간 범위 (초)", 1, 20, 10)

        t = np.linspace(0, t_max, 300)
        x = x0 + v0 * t + 0.5 * a * t**2
        v = v0 + a * t

        st.subheader("시간에 따른 위치와 속도")
        st.write(f"최종 위치: {x[-1]:.2f} m")
        st.write(f"최종 속도: {v[-1]:.2f} m/s")

        fig, ax = plt.subplots(2, 1, figsize=(6, 6))
        ax[0].plot(t, x, 'b')
        ax[0].set_ylabel("위치 (m)")
        ax[0].set_title("위치 vs 시간")

        ax[1].plot(t, v, 'r')
        ax[1].set_xlabel("시간 (s)")
        ax[1].set_ylabel("속도 (m/s)")
        ax[1].set_title("속도 vs 시간")

        st.pyplot(fig)

    elif exp == '단진자운동':
        st.title("단진자 주기 시뮬레이션")

        L = st.slider("줄의 길이 (m)", 0.1, 10.0, 1.0, 0.1)
        g = 9.8
        T = 2 * np.pi * np.sqrt(L / g)
        st.write(f"진자의 주기 T: {T:.2f} 초")

        t = np.linspace(0, 2 * T, 500)
        theta_0 = np.radians(15)
        theta = theta_0 * np.cos(np.sqrt(g / L) * t)
        x = L * np.sin(theta)

        fig, ax = plt.subplots()
        ax.plot(t, x)
        ax.set_title("진자의 가로 위치 vs 시간")
        ax.set_xlabel("시간 (s)")
        ax.set_ylabel("가로 위치 (m)")
        ax.grid(True)

        st.pyplot(fig)
