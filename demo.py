import pandas as pd
import streamlit as st
import numpy as np
import math

def load_data():
	df = pd.read_csv("./db.csv")
	df['month'] = df.apply(lambda x: x['date'].split(".")[1] + '월', axis = 1)
	return df
	
def convert_into_minute(game_time):
    hour = int(game_time.split(":")[0])* 60 
    minute = int(game_time.split(":")[1]) 
    sec = int(game_time.split(":")[2])/60
    return hour + minute + sec

def get_average_stat(data, by, min_game=1):
    by_korean = '챔피언' if by == 'champion' else '플레이어'
    data['cs_per_min'] = data.apply(lambda x : x['cs'] / convert_into_minute(x.game_time), axis = 1)
    data['damage_dealt_per_min'] = data.apply(lambda x : x['damage_dealt'] / convert_into_minute(x.game_time), axis = 1)
    data['sight_score_per_min'] = data.apply(lambda x : x['sight_score'] / convert_into_minute(x.game_time), axis = 1)
	
    df = data[[by,'kill','death','assist', 'cs', 'cs_per_min','win', 'damage_dealt_per_min', 'sight_score_per_min']].groupby(by).mean().reset_index()
	
    game_played = data[[by,'game_no']].groupby(by).count().reset_index()
    df = df.merge(game_played, on=by,how='inner')
    df = df[df['game_no']>=min_game]
	
    df['kda'] = df.apply(lambda x : (x.kill + x.assist)/max(x.death,1), axis = 1)
    df.columns = [by_korean, '평균 킬', '평균 데스', '평균 어시스트', '평균 cs', '평균 분당 cs', '승률','평균 분당 딜량', '평균 분당 시야점수', '총 플레이 횟수', 'KDA']
    df = df[[by_korean, '평균 킬', '평균 데스', '평균 어시스트', '평균 cs', '평균 분당 cs','평균 분당 딜량', '평균 분당 시야점수', 'KDA', '승률', '총 플레이 횟수']]
    return df

def get_player_stat(df, player, position=None, min_game=1, month = '전체'):
    data = df if month == '전체' else df[df['month'] == month]
    data = data[(data['player']== player) & (data['position']==position)] if position is not None else data[(data['player']== player)] 
    
    stat = get_average_stat(data, by='champion', min_game=min_game)
    
    return stat

def get_champion_stat(df, position=None, min_game=1, month = '전체'):
    data = df if month == '전체' else df[df['month'] == month]
    data = data[(data['position']==position)] if position is not None else data
    
    stat = get_average_stat(data, by='champion', min_game=min_game)
    
    return stat

def get_player_ranking(df, position=None, min_game=1, month='전체'):
    data = df if month == '전체' else df[df['month'] == month]
    data = data[(data['position']==position)] if position is not None else data
	
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
months = ['전체']+df.month.unique().tolist()
players = sorted(['강윤모', '김대현', '이건주', '이상훈','고지성', '송기완','김성원', '김예솔', '김윤후', '박은규', '김시은', '유지훈', '이동현', '이유림', '이상현', '이준혁', '장채린', '황지나', '최원태', '한경훈'])
positions = ['전체', '탑', '정글', '미드', '원딜', '서포터']
orders = ['플레이어', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','평균 분당 cs','평균 분당 딜량', '평균 분당 시야점수','KDA', '승률', '총 플레이 횟수']

st.sidebar.title('내전방 스탯 기록 (20240601 19시 업데이트)')
st.sidebar.markdown("# Team of The Month")
month_totm = st.sidebar.selectbox('T.O.T.M 월 선택:', months)
if st.sidebar.button('T.O.T.M 보기'):
	st.write('T.O.T.M 보기')
	for pos in ['탑', '정글', '미드', '원딜', '서포터']:
		player_score = {player: 1 for player in players}
		data = get_player_ranking(df, pos, min_game=5, month=month_totm)
		sorted_data = data.sort_values(by=['KDA', '총 플레이 횟수'], axis=0, ascending=False).reset_index()
		sorted_data.index = sorted_data.index.astype(int)
		for player in players:
			if player in sorted_data['플레이어'].tolist():
				player_score[player] *= (sorted_data[sorted_data['플레이어']==player]['KDA'].tolist()[0]) 
		
		sorted_data = data.sort_values(by=['승률', '총 플레이 횟수'], axis=0, ascending=False).reset_index(drop=True)
		sorted_data.index = sorted_data.index.astype(int)
		for player in players:
			if player in sorted_data['플레이어'].tolist():
				player_score[player] *= (sorted_data[sorted_data['플레이어']==player]['승률'].tolist()[0])
			
		sorted_data = data.sort_values(by=['총 플레이 횟수', '총 플레이 횟수'], axis=0, ascending=False).reset_index()
		sorted_data.index = sorted_data.index.astype(int)
		for player in players:
			if player in sorted_data['플레이어'].tolist():
				player_score[player] *= math.log(sorted_data[sorted_data['플레이어']==player]['총 플레이 횟수'].tolist()[0])

		sorted_data = data.sort_values(by=['평균 분당 딜량', '총 플레이 횟수'], axis=0, ascending=False).reset_index()
		sorted_data.index = sorted_data.index.astype(int)
		for player in players:
			if player in sorted_data['플레이어'].tolist():
				player_score[player] *= (sorted_data[sorted_data['플레이어']==player]['평균 분당 딜량'].tolist()[0])

		sorted_data = data.sort_values(by=['평균 분당 cs', '총 플레이 횟수'], axis=0, ascending=False).reset_index()
		sorted_data.index = sorted_data.index.astype(int)
		for player in players:
			if player in sorted_data['플레이어'].tolist():
				player_score[player] *= (sorted_data[sorted_data['플레이어']==player]['평균 분당 cs'].tolist()[0])
		
		
		sorted_data = data.sort_values(by=['평균 분당 시야점수', '총 플레이 횟수'], axis=0, ascending=False).reset_index()
		for player in players:
			if player in sorted_data['플레이어'].tolist():
				player_score[player] *= (sorted_data[sorted_data['플레이어']==player]['평균 분당 시야점수'].tolist()[0])
		st.write(pos)
		st.write(list(dict(sorted(player_score.items(), key = lambda x: x[1], reverse=True)))[:3])
	
st.sidebar.markdown("-----")
st.sidebar.markdown("# 플레이어 랭킹")


position = st.sidebar.selectbox('포지션:', positions)
order = st.sidebar.selectbox('랭킹 정렬 순:', orders)
min_game = st.sidebar.slider('최소 게임 수', min_value=1, max_value=max(df.game_no) + 1, value=1, step=1)
month_rank = st.sidebar.selectbox('월 선택:', months)
if st.sidebar.button('플레이어 랭킹 보기'):
	st.title(f"{position} 포지션 랭킹 ({month_rank})")
	st.write(f"정렬: {order} 순")
	data = get_player_ranking(df, min_game=min_game, month=month_rank) if position == '전체' else get_player_ranking(df, position, min_game=min_game, month=month_rank)
	data = data[data['플레이어'].isin(players)]
	ascend = False if order not in  ['플레이어', '평균 데스'] else True
	data = data.sort_values(by=[order], axis=0, ascending=ascend).reset_index(drop=True)
	style = {}
	for column in data.select_dtypes(include=['float']).columns:
	    style[column] = "{:.2f}".format
	formatted_df = data.style.format(style)
	st.table(formatted_df)


st.sidebar.markdown("-----")
st.sidebar.markdown("# 포지션별 챔피언 스탯")

position_champ = st.sidebar.selectbox('포지션:  ', positions)
order_champ = st.sidebar.selectbox('랭킹 정렬 순:  ', ['챔피언', '평균 킬', '평균 데스', '평균 어시스트', '평균 cs','평균 분당 cs','평균 분당 딜량', '평균 분당 시야점수','KDA', '승률', '총 플레이 횟수'])
min_game_champ = st.sidebar.slider('최소 게임 수:  ', min_value=1, max_value=max(df.game_no) + 1, value=1, step=1)
month_champ = st.sidebar.selectbox('월 선택:  ', months)

if st.sidebar.button('포지션별 챔피언 스탯 보기'):
	st.title(f"{position} 챔피언 랭킹 ({month_rank})")
	st.write(f"정렬: {order_champ} 순")
	data = get_champion_stat(df, min_game=min_game_champ, month=month_champ) if position_champ == '전체' else get_champion_stat(df,  position_champ, min_game=min_game_champ, month=month_champ)
	
	ascend = False if order_champ not in  ['챔피언', '평균 데스'] else True
	data = data.sort_values(by=[order_champ], axis=0, ascending=ascend).reset_index(drop=True)
	style = {}
	for column in data.select_dtypes(include=['float']).columns:
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
month_stat = st.sidebar.selectbox('월 선택: ', months)
if st.sidebar.button(f'플레이어 스탯 보기'):
	st.title(f"{player_stat} {position_stat} 스탯")
	st.write(f"정렬: {order_stat} 순")
	
	data = get_player_stat(df, player_stat, min_game=min_game_stat, month=month_stat) if position_stat == '전체' else get_player_stat(df, player_stat, position_stat, min_game=min_game_stat, month=month_stat)
	
	ascend = False if order_stat not in  ['챔피언', '평균 데스'] else True
	data = data.sort_values(by=[order_stat], axis=0, ascending=ascend).reset_index(drop=True)
	style = {}
	for column in data.select_dtypes(include=['float']).columns:
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
	for column in data.select_dtypes(include=['float']).columns:
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
	for column in data.select_dtypes(include=['float']).columns:
	    style[column] = "{:.2f}".format
	formatted_df = data.style.format(style)
	st.table(formatted_df)
