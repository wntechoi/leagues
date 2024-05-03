import pandas as pd
import streamlit as st
import numpy as np

def load_data():
	df = pd.read_csv("./db.csv")
	return df
	

df = load_data()

st.markdown("# 내전 기록 등록")
with st.form('내전등록'):
	sorted_df = df.sort_values(by = ['date', 'game_no'], ascending=False).reset_index(drop=True)
	last_match = sorted_df['game_no'][0]
	last_date = sorted_df['date'][0]
	t1 = df[(df['game_no'] == last_match) & (df['team'] == 1)].player.tolist()
	t2 = df[(df['game_no'] == last_match) & (df['team'] == 0)].player.tolist()
	st.markdown(f"# 내전 기록 등록하기")
	st.markdown(f"마지막 업데이트된 내전은 **{last_date}** 펼쳐진")
	st.markdown(f"**{t1[0]}, {t1[1]}, {t1[2]}, {t1[3]}, {t1[4]}** vs **{t2[0]}, {t2[1]}, {t2[2]}, {t2[3]}, {t2[4]}**의 매치입니다.")
	st.markdown(f"위 내전 이후의 내전 기록을 등록해주세요.")
	st.markdown("------")
	df_wait = pd.read_csv("./db_wait.csv")
	sorted_df_wait = df_wait.sort_values(by = ['date', 'game_no'], ascending=False).reset_index(drop=True)
	st.markdown(f"등록 대기중인 내전 {len(df_wait.date.unique().tolist())}건")

	game_no = last_match
	if df_wait.date.unique().tolist():
		last_match_wait = sorted_df_wait['game_no'][0]
		game_no =last_match_wait
		last_date_wait = sorted_df_wait['date'][0]
		t1_wait = sorted_df_wait[(sorted_df_wait['game_no'] == last_match_wait) & (sorted_df_wait['team'] == 1)].player.tolist()
		t2_wait = sorted_df_wait[(sorted_df_wait['game_no'] == last_match_wait) & (sorted_df_wait['team'] == 0)].player.tolist()
		st.markdown(f"마지막 등록 요청된 내전은 **{last_date_wait}** 펼쳐진")
		st.markdown(f"**{t1_wait[0]}, {t1_wait[1]}, {t1_wait[2]}, {t1_wait[3]}, {t1_wait[4]}** vs **{t2_wait[0]}, {t2_wait[1]}, {t2_wait[2]}, {t2_wait[3]}, {t2_wait[4]}**의 매치입니다.")
		st.markdown(f"위 내전 이후의 내전 기록을 등록해주세요.")
		
	st.markdown("------")
	st.markdown("# 신규 내전 등록")
	team_ls = [0,0,0,0,0,1,1,1,1,1]
	game_date = st.text_input("경기 날짜 등록 (xxxx.xx.xx 형태)")
	game_date_ls = [game_date] * 10
	win_team = st.text_input("승리팀 (1팀 or 2팀)")
	last_match_ls = [game_no + 1]*10
	if win_team == 1:
		win_team_ls = [1,1,1,1,1,0,0,0,0,0]
	else:
		win_team_ls = [0,0,0,0,0,1,1,1,1,1]
		
	game_time = st.text_input("경기 플레잉 타임 (x:xx:xx 시간:분:초 형식)")
	game_time_ls = [game_time] * 10
	col1, col2= st.columns(2)
	with col1:
		st.write(f'1팀 기록 등록')
		t1p1 = st.text_input("팀1 플레이어1 이름")
		t1p1_pos = st.text_input("팀1 플레이어1 포지션")
		t1p1_champ = st.text_input("팀1 플레이어1 챔피언")
		t1p1_kill = st.text_input("팀1 플레이어1 킬")
		t1p1_death = st.text_input("팀1 플레이어1 데스")
		t1p1_assist = st.text_input("팀1 플레이어1 어시스트")
		t1p1_cs = st.text_input("팀1 플레이어1 cs")
		t1p1_damage = st.text_input("팀1 플레이어1 딜량")
		t1p1_vision = st.text_input("팀1 플레이어1 시야점수")
		st.markdown("----")
		t1p2 = st.text_input("팀1 플레이어2 이름")
		t1p2_pos = st.text_input("팀1 플레이어2 포지션")
		t1p2_champ = st.text_input("팀1 플레이어2 챔피언")
		t1p2_kill = st.text_input("팀1 플레이어2 킬")
		t1p2_death = st.text_input("팀1 플레이어2 데스")
		t1p2_assist = st.text_input("팀1 플레이어2 어시스트")
		t1p2_cs = st.text_input("팀1 플레이어2 cs")
		t1p2_damage = st.text_input("팀1 플레이어2 딜량")
		t1p2_vision = st.text_input("팀1 플레이어2 시야점수")
		st.markdown("----")
		t1p3 = st.text_input("팀1 플레이어3 이름")
		t1p3_pos = st.text_input("팀1 플레이어3 포지션")
		t1p3_champ = st.text_input("팀1 플레이어3 챔피언")
		t1p3_kill = st.text_input("팀1 플레이어3 킬")
		t1p3_death = st.text_input("팀1 플레이어3 데스")
		t1p3_assist = st.text_input("팀1 플레이어3 어시스트")
		t1p3_cs = st.text_input("팀1 플레이어3 cs")
		t1p3_damage = st.text_input("팀1 플레이어3 딜량")
		t1p3_vision = st.text_input("팀1 플레이어3 시야점수")
		st.markdown("----")
		t1p4 = st.text_input("팀1 플레이어4 이름")
		t1p4_pos = st.text_input("팀1 플레이어4 포지션")
		t1p4_champ = st.text_input("팀1 플레이어4 챔피언")
		t1p4_kill = st.text_input("팀1 플레이어4 킬")
		t1p4_death = st.text_input("팀1 플레이어4 데스")
		t1p4_assist = st.text_input("팀1 플레이어4 어시스트")
		t1p4_cs = st.text_input("팀1 플레이어4 cs")
		t1p4_damage = st.text_input("팀1 플레이어4 딜량")
		t1p4_vision = st.text_input("팀1 플레이어4 시야점수")
		st.markdown("----")
		t1p5 = st.text_input("팀1 플레이어5 이름")
		t1p5_pos = st.text_input("팀1 플레이어5 포지션")
		t1p5_champ = st.text_input("팀1 플레이어5 챔피언")
		t1p5_kill = st.text_input("팀1 플레이어5 킬")
		t1p5_death = st.text_input("팀1 플레이어5 데스")
		t1p5_assist = st.text_input("팀1 플레이어5 어시스트")
		t1p5_cs = st.text_input("팀1 플레이어5 cs")
		t1p5_damage = st.text_input("팀1 플레이어5 딜량")
		t1p5_vision = st.text_input("팀1 플레이어5 시야점수")
	
	with col2:
		st.write(f'2팀 기록 등록')
		t2p1 = st.text_input("팀2 플레이어1 이름")
		t2p1_pos = st.text_input("팀2 플레이어1 포지션")
		t2p1_champ = st.text_input("팀2 플레이어1 챔피언")
		t2p1_kill = st.text_input("팀2 플레이어1 킬")
		t2p1_death = st.text_input("팀2 플레이어1 데스")
		t2p1_assist = st.text_input("팀2 플레이어1 어시스트")
		t2p1_cs = st.text_input("팀2 플레이어1 cs")
		t2p1_damage = st.text_input("팀2 플레이어1 딜량")
		t2p1_vision = st.text_input("팀2 플레이어1 시야점수")
		st.markdown("----")
		t2p2 = st.text_input("팀2 플레이어2 이름")
		t2p2_pos = st.text_input("팀2 플레이어2 포지션")
		t2p2_champ = st.text_input("팀2 플레이어2 챔피언")
		t2p2_kill = st.text_input("팀2 플레이어2 킬")
		t2p2_death = st.text_input("팀2 플레이어2 데스")
		t2p2_assist = st.text_input("팀2 플레이어2 어시스트")
		t2p2_cs = st.text_input("팀2 플레이어2 cs")
		t2p2_damage = st.text_input("팀2 플레이어2 딜량")
		t2p2_vision = st.text_input("팀2 플레이어2 시야점수")
		st.markdown("----")
		t2p3 = st.text_input("팀2 플레이어3 이름")
		t2p3_pos = st.text_input("팀2 플레이어3 포지션")
		t2p3_champ = st.text_input("팀2 플레이어3 챔피언")
		t2p3_kill = st.text_input("팀2 플레이어3 킬")
		t2p3_death = st.text_input("팀2 플레이어3 데스")
		t2p3_assist = st.text_input("팀2 플레이어3 어시스트")
		t2p3_cs = st.text_input("팀2 플레이어3 cs")
		t2p3_damage = st.text_input("팀2 플레이어3 딜량")
		t2p3_vision = st.text_input("팀2 플레이어3 시야점수")
		st.markdown("----")
		t2p4 = st.text_input("팀2 플레이어4 이름")
		t2p4_pos = st.text_input("팀2 플레이어4 포지션")
		t2p4_champ = st.text_input("팀2 플레이어4 챔피언")
		t2p4_kill = st.text_input("팀2 플레이어4 킬")
		t2p4_death = st.text_input("팀2 플레이어4 데스")
		t2p4_assist = st.text_input("팀2 플레이어4 어시스트")
		t2p4_cs = st.text_input("팀2 플레이어4 cs")
		t2p4_damage = st.text_input("팀2 플레이어4 딜량")
		t2p4_vision = st.text_input("팀2 플레이어4 시야점수")
		st.markdown("----")
		t2p5 = st.text_input("팀2 플레이어5 이름")
		t2p5_pos = st.text_input("팀2 플레이어5 포지션")
		t2p5_champ = st.text_input("팀2 플레이어5 챔피언")
		t2p5_kill = st.text_input("팀2 플레이어5 킬")
		t2p5_death = st.text_input("팀2 플레이어5 데스")
		t2p5_assist = st.text_input("팀2 플레이어5 어시스트")
		t2p5_cs = st.text_input("팀2 플레이어5 cs")
		t2p5_damage = st.text_input("팀2 플레이어5 딜량")
		t2p5_vision = st.text_input("팀2 플레이어5 시야점수")
	players = [t1p1, t1p2, t1p3, t1p4, t1p5, t2p1, t2p2, t2p3, t2p4, t2p5]
	positions = [t1p1_pos, t1p2_pos, t1p3_pos, t1p4_pos, t1p5_pos, t2p1_pos, t2p2_pos, t2p3_pos, t2p4_pos, t2p5_pos]
	champions = [t1p1_champ, t1p2_champ, t1p3_champ, t1p4_champ, t1p5_champ, t2p1_champ, t2p2_champ, t2p3_champ, t2p4_champ, t2p5_champ]
	kills = [t1p1_kill, t1p2_kill, t1p3, t1p4_kill, t1p5, t2p1_kill, t2p2_kill, t2p3_kill, t2p4_kill, t2p5_kill]
	deaths= [t1p1_death, t1p2_death, t1p3_death, t1p4_death, t1p5_death, t2p1_death, t2p2_death, t2p3_death, t2p4_death, t2p5_death]
	assists= [t1p1_assist, t1p2_assist, t1p3_assist, t1p4_assist, t1p5_assist, t2p1_assist, t2p2_assist, t2p3_assist, t2p4_assist, t2p5_assist]
	cs= [t1p1_cs, t1p2_cs, t1p3_cs, t1p4_cs, t1p5_cs, t2p1_cs, t2p2_cs, t2p3_cs, t2p4_cs, t2p5_cs]
	damage= [t1p1_damage, t1p2_damage, t1p3_damage, t1p4_damage, t1p5_damage, t2p1_damage, t2p2_damage, t2p3_damage, t2p4_damage, t2p5_damage]
	vision= [t1p1_vision, t1p2_vision, t1p3_vision, t1p4_vision, t1p5_vision, t2p1_vision, t2p2_vision, t2p3_vision, t2p4_vision, t2p5_vision]
	submitted = st.form_submit_button('내전 기록 등록 신청')
	
if submitted:
	if not game_date or not win_team or not game_time or ("" in players) or ("" in kills) or ("" in deaths) or ("" in assists) or ("" in cs) or ("" in damage) or ("" in vision):
		st.error("모든 정보를 다 채워주세요")
	else:
		new_data = pd.DataFrame({"player": players, "position": positions, "champion": champions,	"kill": kills, "death": deaths, "assist": assists, "cs": cs, "win": win_team_ls, "team": team_ls, "game_no": last_match_ls, "date": game_date_ls, "game_time": game_time_ls, "damage_dealt": damage, "sight_score": vision})
		new_df = pd.concat([df_wait, new_data], ignore_index = True)
		st.table(new_df)
		new_df.to_csv("./db_wait.csv", index=False, encoding='utf-8-sig')
		st.write("등록되었습니다. 사이트 재접속 해주세요")
