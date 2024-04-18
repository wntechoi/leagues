import pandas as pd
import streamlit as st
import numpy as np

def load_data():
	df = pd.read_csv("./db.csv")
	return df
	
def convert_into_minute(game_time):
    hour = int(game_time.split(":")[0])* 60 
    minute = int(game_time.split(":")[1]) 
    sec = int(game_time.split(":")[2])/60
    return hour + minute + sec

def get_average_stat(data, by, min_game=1):
    by_korean = '챔피언' if by == 'champion' else '플레이어'
    data['cs_per_min'] = data.apply(lambda x : x['cs'] / convert_into_minute(x.game_time), axis = 1)
	
    df = data[[by,'kill','death','assist', 'cs', 'cs_per_min','win', 'damage_dealt', 'sight_score']].groupby(by).mean().reset_index()
	
    game_played = data[[by,'game_no']].groupby(by).count().reset_index()
    df = df.merge(game_played, on=by,how='inner')
    df = df[df['game_no']>=min_game]
	
    df['kda'] = df.apply(lambda x : (x.kill + x.assist)/max(x.death,1), axis = 1)
    df.columns = [by_korean, '평균 킬', '평균 데스', '평균 어시스트', '평균 cs', '평균 분당 cs', '승률','평균 딜량', '평균 시야점수', '총 플레이 횟수', 'KDA']
    df = df[[by_korean, '평균 킬', '평균 데스', '평균 어시스트', '평균 cs', '평균 분당 cs','평균 딜량', '평균 시야점수', 'KDA', '승률', '총 플레이 횟수']]
    return df

def get_player_stat(df, player, position=None, min_game=1):
    data = df[(df['player']== player) & (df['position']==position)] if position is not None else df[(df['player']== player)] 
    
    stat = get_average_stat(data, by='champion', min_game=min_game)
    
    return stat


def get_player_ranking(df, position=None, min_game=1):
    data = df[(df['position']==position)] if position is not None else df
    data = get_average_stat(data, by='player', min_game=min_game)
    return data


def get_player_matchup_df(df, p1, p2, position):
    data_p1 = df[(df['player'] == p1) & (df['position']==position)]
    data_p2 = df[(df['player'] == p2) & (df['position']==position)]
    data = data_p1.merge(data_p2, on ='game_no', how='inner')
    data = data[data['team_x'] != data['team_y']]
    return data


def same_team_win_percentage(df, p1, p2):
    data_p1 = df[(df['player'] == p1)]
    data_p2 = df[(df['player'] == p2)]
    data = data_p1.merge(data_p2, on ='game_no', how='inner')
    data = data[data['team_x'] == data['team_y']]
    return np.mean(data.win_x)


df = load_data()
st.sidebar.title('내전방 스탯 기록 20240417')

st.sidebar.markdown("# 플레이어 랭킹")
players = sorted(df.player.unique().tolist())
positions = ['전체', '탑', '정글', '미드', '원딜', '서포터']
orders = ['플레이어', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','평균 분당 cs','평균 딜량', '평균 시야점수','KDA', '승률', '총 플레이 횟수']
position = st.sidebar.selectbox('포지션:', positions)
order = st.sidebar.selectbox('랭킹 정렬 순:', orders)
min_game = st.sidebar.slider('최소 게임 수', min_value=1, max_value=max(df.game_no) + 1, value=1, step=1)
if st.sidebar.button('플레이어 랭킹 보기'):
	st.title(f"{position} 랭킹")
	st.write(f"{order} 순")
	data = get_player_ranking(df, min_game=min_game) if position == '전체' else get_player_ranking(df, position, min_game=min_game)
	
	ascend = False if order not in  ['플레이어', '평균 데스'] else True
	data = data.sort_values(by=[order], axis=0, ascending=ascend).reset_index(drop=True)
	st.table(data)


st.sidebar.markdown("--------")
st.sidebar.markdown("# 개인 스탯")
player_stat = st.sidebar.selectbox('플레이어:', players)
position_stat = st.sidebar.selectbox('포지션 선택:', positions)
orders_stat = ['챔피언', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','평균 분당 cs','평균 딜량', '평균 시야점수','KDA', '승률', '총 플레이 횟수']
order_stat = st.sidebar.selectbox('스탯 정렬 순:', orders_stat)
min_game_stat = st.sidebar.slider('최소 게임 수 ', min_value=1, max_value=max(df.game_no) + 1, value=1, step=1)

if st.sidebar.button('플레이어 스탯 보기'):
	st.title(f"{player_stat} {position_stat} 스탯")
	st.write(f"{order_stat} 순")
	
	data = get_player_stat(df, player_stat, min_game=min_game_stat) if position_stat == '전체' else get_player_stat(df, player_stat, position_stat, min_game=min_game_stat)
	
	ascend = False if order_stat not in  ['챔피언', '평균 데스'] else True
	data = data.sort_values(by=[order_stat], axis=0, ascending=ascend).reset_index(drop=True)
	st.table(data)
	
