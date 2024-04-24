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
    data_p1 = df[(df['player'] == p1) & (df['position']==position)] if position !='전체' else df[(df['player'] == p1)]
    data_p2 = df[(df['player'] == p2) & (df['position']==position)] if position !='전체' else df[(df['player'] == p2)]
    data = data_p1.merge(data_p2, on ='game_no', how='inner')
    data = data[data['team_x'] != data['team_y']]
    data['win_or_not_x'] = data.apply(lambda x: '승리' if x['win_x'] == 1 else '패배', axis=1)
    data['win_or_not_y'] = data.apply(lambda x: '승리' if x['win_y'] == 1 else '패배', axis=1)
    return data


def same_team_win_percentage(df, p1, p2):
    data_p1 = df[(df['player'] == p1)]
    data_p2 = df[(df['player'] == p2)]
    data = data_p1.merge(data_p2, on ='game_no', how='inner')
    data = data[data['team_x'] == data['team_y']]
    data['win_or_not_x'] = data.apply(lambda x: '승리' if x['win_x'] == 1 else '패배', axis=1)
    return data


df = load_data()
st.sidebar.title('내전방 스탯 기록 (20240424 21시 업데이트)')

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
	style = {}
	for column in data.columns:
	    style[column] = "{:.2f}".format
	formatted_df = data.style.format(style)
	st.table(formatted_df)


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
	style = {}
	for column in data.columns:
	    style[column] = "{:.2f}".format
	formatted_df = data.style.format(style)
	st.table(formatted_df)


st.sidebar.markdown("--------")
st.sidebar.markdown("# 매치업 비교")
player1 = st.sidebar.selectbox('플레이어 1:', players)
player2 = st.sidebar.selectbox('플레이어 2:', players)
position = st.sidebar.selectbox('매치업 포지션:', positions)
if st.sidebar.button('매치업 보기'):
	data = get_player_matchup_df(df, player1, player2, position)
	st.markdown(f"# {player1} vs {player2}")
	st.markdown(f"|-|승률|-|\n|--|--|--|\n|{player1}|{np.mean(data.win_x)} : {np.mean(data.win_y)}|{player2}|\n|게임 횟수 | {len(data)} |- |")
	col1, col2= st.columns(2)
	with col1:
	    st.header(f'{player1} 매치 기록')
    
	with col2:
	    st.header(f'{player2} 매치 기록')
	data = data[['position_x', 'champion_x', 'kill_x', 'death_x', 'assist_x','cs_x','damage_dealt_x', 'sight_score_x', 'win_or_not_x','game_time_x', 'win_or_not_y', 'position_y', 'champion_y', 'kill_y', 'death_y', 'assist_y','cs_y','damage_dealt_y', 'sight_score_y']]
	data.columns = [f'포지션_{player1}', f'챔피언_{player1}', f'킬_{player1}', f'데스_{player1}', f'어시스트_{player1}', f'cs_{player1}',f'딜량_{player1}', f'시야점수_{player1}', f'승리여부_{player1}','게임 시간',f'승리여부_{player2}',f'포지션_{player2}', f'챔피언_{player2}', f'킬_{player2}', f'데스_{player2}', f'어시스트_{player2}', f'cs_{player2}',f'딜량_{player2}', f'시야점수_{player2}']
	style = {}
	for column in data.columns:
            style[column] = "{:.2f}".format
	formatted_df = data.style.format(style)
	st.table(formatted_df)

st.sidebar.markdown("--------")
st.sidebar.markdown("# 팀 궁합")
p1 = st.sidebar.selectbox('플레이어 1: ', players)
p2 = st.sidebar.selectbox('플레이어 2: ', players)
if st.sidebar.button('팀 궁합 보기'):
	data = same_team_win_percentage(df, p1, p2)
	st.markdown(f"# {p1} + {p2}")
	st.markdown(f"총 **{len(data)}번** 같은 팀을 해서 **{len(data[data['win_x']==1])}번** 이겨 **{np.mean(data.win_x) * 100}**%의 승률을 기록하고 있습니다")
	col1, col2= st.columns(2)
	with col1:
	    st.header(f'{p1} 매치 기록')
    
	with col2:
	    st.header(f'{p2} 매치 기록')
	data = data[['win_or_not_x','position_x', 'champion_x', 'kill_x', 'death_x', 'assist_x','cs_x','damage_dealt_x', 'sight_score_x','game_time_x', 'position_y', 'champion_y', 'kill_y', 'death_y', 'assist_y','cs_y','damage_dealt_y', 'sight_score_y']]
	data.columns = [f'승리여부',f'포지션_{p1}', f'챔피언_{p1}', f'킬_{p1}', f'데스_{p1}', f'어시스트_{p1}', f'cs_{p1}',f'딜량_{p1}', f'시야점수_{p1}', '게임 시간',f'포지션_{p2}', f'챔피언_{p2}', f'킬_{p2}', f'데스_{p2}', f'어시스트_{p2}', f'cs_{p2}',f'딜량_{p2}', f'시야점수_{p2}']
	style = {}
	for column in data.columns:
	    style[column] = "{:.2f}".format
	formatted_df = data.style.format(style)
	st.table(formatted_df)
