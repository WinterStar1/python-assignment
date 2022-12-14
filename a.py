import tkinter
import time
import tkinter.messagebox
import random

maze=[
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,0],  # 리스트를 통해 벽, 움직일 수 있는 공간,보스,구출할 캐릭터 등 위치 정의
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,2,1,3,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0]
    ]

def draw_p(): # 벽,보스,캐릭터,바닥 등 표시 함수
    for y in range(9):
        for x in range(10):
            if maze[y][x] > 0:
                cvs.create_image(x*80+79,y*80+79,image=img_p[maze[y][x]])
            else :
                cvs.create_image(x*80+79,y*80+79,image=wall)
                
key="" # 키 입력 변수 선언

def key_down(e): #키를 눌렀을때 실행할 함수 정의
    global key
    key=e.keysym
def key_up(e): #키를 뗐을때 실행할 함수 정의
    global key
    key = ""

def close_window(): #화면을 닫는 함수 정의
    root.destroy()

mx=1  #플레이어의 캐릭터 시작위치 설정
my=5
floor=4

def main_proc(): #움직임을 처리하는 함수 정의
    global mx,my,floor
    if key=="Up"and maze[my-1][mx]>0:
        my=my-1
    if key=="Down"and maze[my+1][mx]>0:
        my=my+1
    if key=="Left"and maze[my][mx-1]>0:
        mx=mx-1
    if key=="Right"and maze[my][mx+1]>0:
        mx=mx+1
    if maze[my][mx]==1:
        maze[my][mx]=5
        floor=floor+1 #움직인 횟수 카운트
        if floor==10:
            cvs.update()
            tkinter.messagebox.showinfo("알림","몬스터가 나타났다!")
            close_window()
    cvs.coords("하야사카",mx*80+40,my*80+40)
    root.after(100,main_proc)
    
root=tkinter.Tk()
root.title("이동")
root.bind("<KeyPress>",key_down) #윈도우 객체생성,키입력에 따른 실행 함수 정의
root.bind("<KeyRelease>",key_up)
root.resizable(False, False)
cvs=tkinter.Canvas(root,width=880,height=720)
cvs.pack()            
            
wall=tkinter.PhotoImage(file="wall.png")
img_p=[  #리스트를 통해 띄울 사진 정리
    None,
    tkinter.PhotoImage(file="floor.png"),
    tkinter.PhotoImage(file="3.png"),
    tkinter.PhotoImage(file="5.png")
]
draw_p()

img=tkinter.PhotoImage(file="1.png") #플레이어의 캐릭터 로딩
cvs.create_image(mx*80+40,my*80+40,image=img,tag="하야사카")
main_proc()
root.mainloop() #윈도우 표시

FNT = ("Times New Roman", 24) #폰트 정의

class GameCharacter: #클래스 정의
    def __init__(self, name, life, x, y, imgfile, tagname): #생성자
        self.name = name #각 속성에 인수값 대입
        self.life = life
        self.lmax = life
        self.x = x
        self.y = y
        self.img = tkinter.PhotoImage(file=imgfile) #이미지 로딩
        self.tagname = tagname
    
    def draw(self): #이미지 표시 메서드
        x = self.x #x 속성에 x좌표 대입
        y = self.y #y 속성에 y좌표 대입
        canvas.create_image(x, y, image=self.img, tag=self.tagname) #이미지 표시
        canvas.create_text(x, y + 120, text=self.name, font=FNT, fill="navy", tag=self.tagname)
        #문자열 표시(name 속성값)
        canvas.create_text(x, y + 200, text="life{}/{}".format(self.life, self.lmax), font=FNT, fill="red",
                           tag=self.tagname) #문자열 표시(life, lmax속성값)
    
    def attack(self): #공격 처리 수행 메서드
        di = 1 #이미지 이동 방향
        if self.x >= 400: #오른쪽 캐릭터
            di = -1 #이동 방향:왼쪽
        for i in range(5):  # 공격 동작 반복 (옆으로 움직임)
            canvas.coords(self.tagname, self.x + i * 10 * di, self.y) #표시 위치 변경
            canvas.update() #캔버스 업데이트
            time.sleep(0.1) #0.1초 대기
        canvas.coords(self.tagname, self.x, self.y) #이미지 원위치

    def damage(self): #데미지 처리 수행 메서드
        x=random.randint(1,3) #변수 x에 1,2,3 중 하나의 정수 대입
        for i in range(5):  # 데미지 반복 (화면 깜빡임)
            self.draw() #캐릭터 표시 메서드 실행
            canvas.update()
            time.sleep(0.1)
            canvas.delete(self.tagname) #화면 삭제 (우선 지움)
            canvas.update()
            time.sleep(0.1)
        if x == 1: #변수 x가 1일 시 (컴퓨터 공격 선택)
            self.life = self.life - 30 #체력 30 감소
            tkinter.messagebox.showinfo("com : 공격","공격에 성공했습니다!") #메시지 박스 표시
            tkinter.messagebox.showinfo("com : 공격","몬스터는 30의 피해를 입었습니다!")
        elif x == 2: #변수 x가 2일 시 (컴퓨터 방어 선택)
            self.life = self.life - 10
            tkinter.messagebox.showinfo("com : 방어","몬스터는 방어했습니다!")
            tkinter.messagebox.showinfo("com : 방어","몬스터는 10의 피해를 입었습니다!")
        else: #변수 x가 3일 시 (컴퓨터 회피 선택)
            tkinter.messagebox.showinfo("com : 회피","몬스터는 회피했습니다!")
        if self.life > 0: #체력이 0보다 많으면
            self.draw() #캐릭터 표시
        else: #체력이 0 이하이면
            tkinter.messagebox.showinfo("정보","대전이 끝났습니다.")
            
    def debuff(self): #디버프 처리 수행 메서드
        for i in range(5):
            self.draw()
            canvas.update()
            time.sleep(0.1)
            canvas.delete(self.tagname)
            canvas.update()
            time.sleep(0.1)
        self.life = self.life - 15 #체력 15 감소 (계속 공격만 눌러 승리하는 패턴 방지)
        tkinter.messagebox.showinfo("디버프","내 캐릭터는 15의 피해를 입었습니다!")
        if self.life > 0:
            self.draw()
        
    def defence(self): #방어 처리 수행 메서드
        x=random.randint(1,3)
        for i in range(5):
            self.draw()
            canvas.update()
            time.sleep(0.1)
            canvas.delete(self.tagname)
            canvas.update()
            time.sleep(0.1)
        self.life = self.life + 5 #체력 5 회복
        tkinter.messagebox.showinfo("방어","내 캐릭터의 체력이 5 회복되었습니다!")
        if x == 1: #컴퓨터의 선택 : 공격
            self.life = self.life - 10 #체력 10 감소
            tkinter.messagebox.showinfo("com : 공격","방어에 성공했습니다!")
            tkinter.messagebox.showinfo("com : 공격","내 캐릭터는 10의 피해를 입었습니다!")
        elif x == 2: #컴퓨터의 선택 : 방어
            tkinter.messagebox.showinfo("com : 방어","아무 일도 일어나지 않았습니다!")
        else: #컴퓨터의 선택 : 회피
            tkinter.messagebox.showinfo("com : 회피","아무 일도 일어나지 않았습니다!")
        if self.life > 0:
            self.draw()
        else:
            tkinter.messagebox.showinfo("정보","대전이 끝났습니다.")
            
    def evasion(self): #회피 처리 수행 메서드
        x=random.randint(1,3)
        for i in range(5): 
            self.draw()
            canvas.update()
            time.sleep(0.1)
            canvas.delete(self.tagname)
            canvas.update()
            time.sleep(0.1)
        if x == 1:
            tkinter.messagebox.showinfo("com : 공격","회피에 성공했습니다!")
        elif x == 2:
            tkinter.messagebox.showinfo("com : 방어","아무 일도 일어나지 않았습니다!")
        else:
            tkinter.messagebox.showinfo("com : 회피","아무 일도 일어나지 않았습니다!")
        if self.life > 0:
            self.draw()
        else:
            tkinter.messagebox.showinfo("정보","대전이 끝났습니다.")

def click_attack(): #공격 버튼 클릭 처리 함수
    character[0].attack() #내 캐릭터의 공격 처리 메서드 실행
    character[1].damage() #몬스터의 데미지 처리 메서드 실행
    character[0].debuff() #디버프 처리 메서드 실행
    
def click_defence(): #방어 버튼 클릭 처리 함수
    character[1].attack() #몬스터의 공격 처리 메서드 실행
    character[0].defence() #내 캐릭터의 방어 처리 메서드 실행
    
def click_evasion(): #회피 버튼 클릭 처리 함수
    character[1].attack() #몬스터의 공격 처리 메서드 실행
    character[0].evasion() #내 캐릭터의 회피 처리 메서드 실행

root = tkinter.Tk() #윈도우 객체 생성
root.title("전투") #타이틀 화면 지정
canvas = tkinter.Canvas(root, width=800, height=600, bg="white") #캔버스 컴포넌트 생성
canvas.pack() #캔버스 배치

btn_attack = tkinter.Button(text="공격", command=click_attack, height=2, width=10) #공격 버튼 생성
btn_attack.place(x=370, y=160) #위치 설정
btn_defence = tkinter.Button(text="방어", command=click_defence, height=2, width=10) #방어 버튼 생성
btn_defence.place(x=370, y=260) #위치 설정
btn_evasion = tkinter.Button(text="회피", command=click_evasion, height=2, width=10) #회피 버튼 생성
btn_evasion.place(x=370, y=360) #위치 설정

character = [ #리스트로 객체 생성
    GameCharacter("하야사카", 150, 200, 280, "2.png", "LC"), #내 캐릭터 객체
    GameCharacter("이이노", 150, 600, 280, "4.png", "RC") #몬스터 객체
]
character[0].draw() #내 캐릭터 객체의 draw() 메서드 실행
character[1].draw() #몬스터 객체의 draw() 메서드 실행

root.mainloop() #윈도우 표시

maze=[
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,3,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0]
    ]

def draw_p():
    for y in range(9):
        for x in range(10):
            if maze[y][x] > 0:
                cvs.create_image(x*80+79,y*80+79,image=img_p[maze[y][x]])
            else :
                cvs.create_image(x*80+79,y*80+79,image=wall)
                
key=""

def key_down(e):
    global key
    key=e.keysym
def key_up(e):
    global key
    key = ""

def close_window():
    root.destroy()

mx=5
my=5
floor=6

def main_proc():
    global mx,my,floor
    if key=="Up"and maze[my-1][mx]>0:
        my=my-1
    if key=="Down"and maze[my+1][mx]>0:
        my=my+1
    if key=="Left"and maze[my][mx-1]>0:
        mx=mx-1
    if key=="Right"and maze[my][mx+1]>0:
        mx=mx+1
    if maze[my][mx]==1:
        maze[my][mx]=5
        floor=floor+1
        if floor==10:
            cvs.update()
            tkinter.messagebox.showinfo("알림","구출에 성공했다!")
            close_window()
    cvs.coords("하야사카",mx*80+40,my*80+40)
    root.after(100,main_proc)
    
root=tkinter.Tk()
root.title("이동")
root.bind("<KeyPress>",key_down)
root.bind("<KeyRelease>",key_up)
root.resizable(False, False)
cvs=tkinter.Canvas(root,width=880,height=720)
cvs.pack()            
            
wall=tkinter.PhotoImage(file="wall.png")
img_p=[
    None,
    tkinter.PhotoImage(file="floor.png"),
    tkinter.PhotoImage(file="3.png"),
    tkinter.PhotoImage(file="5.png")
]
draw_p()

img=tkinter.PhotoImage(file="1.png")
cvs.create_image(mx*80+40,my*80+40,image=img,tag="하야사카")
main_proc()
root.mainloop()