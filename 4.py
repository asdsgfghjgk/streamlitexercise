import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.title('수준별 물리 실험 그래프 그리기')

# 학년 선택
level = st.slider("난이도", 1, 3, 1)

# 실험 주제
experiments_by_grade = {
    1: ["등가속도 운동", "단진자 운동"],
    2: ["운동량 보존", "옴의 법칙"],
    3: ["빛의 굴절 실험", "도플러 효과"]
}

experiment = st.radio("실험 선택", experiments_by_grade[level])

# 1학년
if level == 1:
    if experiment == "등가속도 운동":
        st.subheader("등가속도 운동")
        a = st.slider("가속도 (m/s²)", -10.0, 10.0, 2.0)
        v0 = st.slider("초기 속도 (m/s)", -20.0, 20.0, 0.0)
        x0 = st.slider("초기 위치 (m)", -50.0, 50.0, 0.0)
        t = np.linspace(0, 10, 300)
        x = x0 + v0 * t + 0.5 * a * t**2
        v = v0 + a * t

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

    elif experiment == "단진자 운동":
        st.subheader("단진자 운동")
        L = st.slider("줄 길이 (m)", 0.1, 10.0, 1.0)
        theta0 = st.slider("초기 각도 (도)", 1.0, 30.0, 10.0)
        g = 9.8
        T = 2 * np.pi * np.sqrt(L / g)
        st.write(f"단진자 주기: {T:.2f} s")

        t = np.linspace(0, 5 * T, 500)
        theta = np.radians(theta0) * np.cos(np.sqrt(g / L) * t)
        x = L * np.sin(theta)

        fig, ax = plt.subplots()
        ax.plot(t, x)
        ax.set_xlabel("시간 (s)")
        ax.set_ylabel("가로 위치 (m)")
        ax.set_title("진자의 가로 위치 vs 시간")
        ax.grid(True)
        st.pyplot(fig)

elif level == 2:
    if experiment == "운동량 보존":
        st.subheader("운동량 보존 시뮬레이션")

        # 입력값
        m1 = st.slider("물체 1 질량 (kg)", 0.1, 10.0, 1.0)
        m2 = st.slider("물체 2 질량 (kg)", 0.1, 10.0, 1.0)
        v1 = st.slider("물체 1 초기 속도 (m/s)", -10.0, 10.0, 5.0)
        v2 = st.slider("물체 2 초기 속도 (m/s)", -10.0, 10.0, -2.0)
        x1_0 = st.slider("물체 1 초기 위치 (m)", -10.0, 10.0, -5.0)
        x2_0 = st.slider("물체 2 초기 위치 (m)", -10.0, 10.0, 5.0)
        t_max = st.slider("시뮬레이션 시간 (초)", 1, 20, 10)

        t = np.linspace(0, t_max, 300)

        # 충돌 시점 계산
        if v1 == v2:
            t_collision = t_max + 1  # 충돌 안 함
        else:
            t_collision = (x2_0 - x1_0) / (v1 - v2)

        t1 = t[t < t_collision]
        t2 = t[t >= t_collision]

        # 위치 계산
        x1 = np.piecewise(t, [t < t_collision, t >= t_collision],
                          [lambda t: x1_0 + v1 * t, lambda t: x1_0 + v1 * t_collision + ((m1 * v1 + m2 * v2) / (m1 + m2)) * (t - t_collision)])
        x2 = np.piecewise(t, [t < t_collision, t >= t_collision],
                          [lambda t: x2_0 + v2 * t, lambda t: x2_0 + v2 * t_collision + ((m1 * v1 + m2 * v2) / (m1 + m2)) * (t - t_collision)])

        # 속도 계산
        v1_arr = np.piecewise(t, [t < t_collision, t >= t_collision],
                              [v1, (m1 * v1 + m2 * v2) / (m1 + m2)])
        v2_arr = np.piecewise(t, [t < t_collision, t >= t_collision],
                              [v2, (m1 * v1 + m2 * v2) / (m1 + m2)])

        # 그래프 출력
        fig, ax = plt.subplots(2, 1, figsize=(6, 6))

        ax[0].plot(t, x1, label="물체 1", color="blue")
        ax[0].plot(t, x2, label="물체 2", color="green")
        ax[0].set_ylabel("위치 (m)")
        ax[0].legend()
        ax[0].set_title("위치 vs 시간")

        ax[1].plot(t, v1_arr, label="물체 1", color="blue")
        ax[1].plot(t, v2_arr, label="물체 2", color="green")
        ax[1].set_xlabel("시간 (s)")
        ax[1].set_ylabel("속도 (m/s)")
        ax[1].legend()
        ax[1].set_title("속도 vs 시간")

        st.pyplot(fig)

    elif experiment == "옴의 법칙":
        st.subheader("옴의 법칙 시뮬레이션")

        # 입력
        R = st.slider("저항 (Ω)", 1.0, 100.0, 10.0)
        V_max = st.slider("최대 전압 (V)", 0.0, 20.0, 10.0)

        V = np.linspace(0, V_max, 100)
        I = V / R

        fig, ax = plt.subplots()
        ax.plot(V, I, color='orange')
        ax.set_xlabel("전압 (V)")
        ax.set_ylabel("전류 (A)")
        ax.set_title("옴의 법칙: 전압 vs 전류")
        ax.grid(True)

        st.pyplot(fig)

elif level == 3:
    if experiment == "빛의 굴절 실험":
        st.subheader("빛의 굴절 실험")
        n1 = st.slider("입사 매질 굴절률", 1.0, 2.5, 1.0)
        n2 = st.slider("굴절 매질 굴절률", 1.0, 2.5, 1.5)
        angle_inc = st.slider("입사각 (도)", 0.0, 89.0, 30.0)

        angle_inc_rad = np.radians(angle_inc)
        try:
            angle_refr_rad = np.arcsin(n1 / n2 * np.sin(angle_inc_rad))
            angle_refr = np.degrees(angle_refr_rad)
            st.write(f"굴절각: {angle_refr:.2f}°")
        except:
            st.write("전반사가 발생했습니다!")

        fig, ax = plt.subplots()
        ax.plot([0, np.cos(angle_inc_rad)], [0, np.sin(angle_inc_rad)], label="입사선")
        if n1 / n2 * np.sin(angle_inc_rad) <= 1:
            ax.plot([0, np.cos(angle_refr_rad)], [0, -np.sin(angle_refr_rad)], label="굴절선")
        ax.axhline(0, color='black', linestyle='--')
        ax.set_aspect('equal')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.legend()
        ax.set_title("빛의 굴절 시뮬레이션")
        st.pyplot(fig)

    elif experiment == "도플러 효과":
        st.subheader("도플러 효과 시뮬레이션")
        vs = st.slider("소리의 속도 (m/s)", 300, 400, 340)
        f0 = st.slider("원래 주파수 (Hz)", 100, 1000, 440)
        v_source = st.slider("소리원 속도 (m/s)", -200, 200, 0)
        v_observer = st.slider("관측자 속도 (m/s)", -200, 200, 0)

        f_obs = f0 * (vs + v_observer) / (vs - v_source)
        st.write(f"관측자가 들은 주파수: {f_obs:.2f} Hz")

        t = np.linspace(0, 0.05, 1000)
        wave_orig = np.sin(2 * np.pi * f0 * t)
        wave_obs = np.sin(2 * np.pi * f_obs * t)

        fig, ax = plt.subplots()
        ax.plot(t, wave_orig, label="원래 파형")
        ax.plot(t, wave_obs, label="관측된 파형", alpha=0.7)
        ax.set_title("도플러 효과: 파형 비교")
        ax.set_xlabel("시간 (s)")
        ax.set_ylabel("진폭")
        ax.legend()
        st.pyplot(fig)
