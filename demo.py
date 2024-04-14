import pandas as pd
import streamlit as st
import numpy as np

def load_data():
	df = pd.read_csv("./data/db.csv")
	return df
	
def get_player_stat_by_champion(df, player):
    data = df[(df['player']== player)]
    stat = data[['champion','kill','death','assist','cs','win']].groupby('champion').mean().reset_index().merge(data[['champion','game_no']].groupby('champion').count().reset_index(), on='champion',how='inner')
	
    stat['kda'] = stat.apply(lambda x : (x.kill + x.assist)/max(x.death,1), axis = 1)
    return stat

def get_player_stat_by_position(df, player, position):
    data = df[(df['player']== player) & (df['position']==position)]
    stat_by_champion = data[['champion','kill','death','assist','cs','win']].groupby('champion').mean().reset_index().merge(data[['champion','game_no']].groupby('champion').count().reset_index(), on='champion',how='inner')
    stat_by_champion['kda'] = stat_by_champion.apply(lambda x : (x.kill + x.assist)/max(x.death,1), axis = 1)
    return stat_by_champion

def get_player_matchup_df(df, p1, p2, position):
    data_p1 = df[(df['player'] == p1) & (df['position']==position)]
    data_p2 = df[(df['player'] == p2) & (df['position']==position)]
    data = data_p1.merge(data_p2, on ='game_no', how='inner')
    data = data[data['team_x'] != data['team_y']]
    return data

def get_player_ranking(df):
    df_count_all = df[['player', 'kill', 'death','assist','cs','win']].groupby("player").mean().reset_index()
    df_count_all.columns = ['player', 'kill', 'death','assist','cs','win_percent']
    df_count_play = df[['player','win']].groupby("player").count().reset_index()
    df_count_play.columns = ['player','count_play']
    data = df_count_all.merge(df_count_play,on='player',how = 'inner')
    data['kda'] = data.apply(lambda x : (x.kill + x.assist)/max(1,x.death), axis = 1)
    return data

def get_player_ranking_by_position(df, position):
    df_count_all = df[(df['position']==position)][['player', 'kill', 'death','assist','cs','win']].groupby("player").mean().reset_index()
    df_count_all.columns = ['player', 'kill', 'death','assist','cs','win_percent']
    df_count_play = df[df['position']==position][['player','win']].groupby("player").count().reset_index()
    df_count_play.columns = ['player','count_play']
    data = df_count_all.merge(df_count_play,on='player',how = 'inner')
    data['kda'] = data.apply(lambda x : (x.kill + x.assist)/max(1,x.death), axis = 1)
    return data

def same_team_win_percentage(df, p1, p2):
    data_p1 = df[(df['player'] == p1)]
    data_p2 = df[(df['player'] == p2)]
    data = data_p1.merge(data_p2, on ='game_no', how='inner')
    data = data[data['team_x'] == data['team_y']]
    return np.mean(data.win_x)



df = load_data()
st.sidebar.title('내전방 스탯 기록 20240413')
st.sidebar.markdown("# 플레이어 랭킹")
players = sorted(df.player.unique().tolist())
positions = ['전체', '탑', '정글', '미드', '원딜', '서포터']
orders = ['플레이어', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','KDA', '승률', '총 플레이 횟수']
position = st.sidebar.selectbox('포지션:', positions)
order = st.sidebar.selectbox('랭킹 정렬 순:', orders)
if st.sidebar.button('플레이어 랭킹 보기'):
	st.title(f"{position} 랭킹")
	st.write(f"{order} 순")
	if position == '전체':
		data = get_player_ranking(df)
		data.columns = ['플레이어', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs', '승률', '총 플레이 횟수', 'KDA']
		data = data[['플레이어', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','KDA', '승률', '총 플레이 횟수']]
	else:
		data = get_player_ranking_by_position(df, position)
		data.columns = ['플레이어', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs', '승률', '총 플레이 횟수', 'KDA']
		data = data[['플레이어', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','KDA', '승률', '총 플레이 횟수']]
	ascend = False if order not in  ['플레이어', '평균 데스'] else True
	data = data.sort_values(by=[order], axis=0, ascending=ascend)
	st.table(data)
st.sidebar.markdown("--------")
st.sidebar.markdown("# 개인 스탯")
player_stat = st.sidebar.selectbox('플레이어:', players)
position_stat = st.sidebar.selectbox('포지션 선택:', positions)
orders_stat = ['챔피언', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','KDA', '승률', '총 플레이 횟수']
order_stat = st.sidebar.selectbox('스탯 정렬 순:', orders_stat)
if st.sidebar.button('플레이어 스탯 보기'):
	st.title(f"{player_stat} {position_stat} 스탯")
	st.write(f"{order_stat} 순")
	if position_stat == '전체':
		data = get_player_stat_by_champion(df, player_stat)
		data.columns = ['챔피언', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs', '승률', '총 플레이 횟수', 'KDA']
		data = data[['챔피언', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','KDA', '승률', '총 플레이 횟수']]
	else:
		data = get_player_stat_by_position(df, player_stat, position_stat)
		data.columns = ['챔피언', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs', '승률', '총 플레이 횟수', 'KDA']
		data = data[['챔피언', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','KDA', '승률', '총 플레이 횟수']]
	ascend = False if order_stat not in  ['챔피언', '평균 데스'] else True
	data = data.sort_values(by=[order_stat], axis=0, ascending=ascend)
	st.table(data)
	