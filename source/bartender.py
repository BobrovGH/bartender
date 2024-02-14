#импорт модулей
import mysql.connector as sql
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkmacosx import Button
from PIL import ImageTk, Image
from sqlalchemy import create_engine
from datetime import datetime
#создание шаблонов цветов, подлкючение локальной БД, функции получения текущего времени
bgc="#4D4D4D"
btc='#828282'
conn=sql.connect(host='ХОСТ',username='ИМЯ ПОЛЬЗОВАТЕЛЯ',password='ПАРОЛЬ',database='bartender')
conn.autocommit = True
cursor=conn.cursor()
def noow():
    now = datetime.now()
    a=str(now.day)+'.'+str(now.month)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+' | '
    return a
#класс дочернего окна для просмотра, изменения и добавления информации о товаре
class WindowInfo(tk.Toplevel):
    def __init__(self, container, selected, new):
        super().__init__(container)
        x=container.winfo_rootx()+50
        y=container.winfo_rooty()+50
        self.geometry('400x600+%s+%s'%(x,y))
        self.grab_set()
        self.overrideredirect(True)
        buttons=[]
        entrys=[]
        #заменает NoneType на null
        for i in range(len(selected)):
            if selected[i]==None: selected[i]='null'
        #заменяет символы для корректной работы sql-запросов
        def rplc(a):
            a=a.replace(',','.').replace('%','').replace('% ','')
            return a
        #преобразует виджет в виджет добавления нового товара
        def new_item():
            for i in range(10):
                entrys[i].config(state='normal')
                buttons[i].destroy()
            entrys[0].delete(0,END)
            entrys[0].insert(0,'ID задаётся базой данной')
            entrys[0].config(state='disabled')
            about_text.config(state='normal',bg='#171717',fg='white')
            buttons[10].destroy()
            buttons[11].destroy()
            name.config(text='Добавление нового товара')
            commit.config(command=insert_item)
            rst.config(text='Очистить поля',command=clear)
        #выход из дочернего окна
        def exit():
            self.destroy()
        #работа кнопок редактирования
        def edit(a):
            if entrys[a]['state'] == 'disabled':
                entrys[a].config(state='normal')
                buttons[a].config(bg=bgc)
            else:
                entrys[a].config(state='disable')
                buttons[a].config(bg='white')
        def editabout():
            if about_text['state']=='disabled':
                about_text.config(state='normal',bg='#171717',fg='white')
                buttons[10].config(bg=bgc)
            else:
                about_text.config(state='disable',bg='#323232',fg='#B1B2B1')
                buttons[10].config(bg='white')
        def editall():
            if b['bg']=='white':
                for i in range (1,10):
                    entrys[i].config(state='normal')
                    buttons[i].config(bg=bgc)
                about_text.config(state='normal',bg='#171717')
                buttons[10].config(bg=bgc)
                buttons[11].config(bg=bgc)
            else:
                for i in range (1,10):
                    entrys[i].config(state='disable')
                    buttons[i].config(bg='white')
                about_text.config(state='disable',bg='#323232')
                buttons[10].config(bg='white')
                buttons[11].config(bg='white')
        #возвращает tulpe с данными из полей
        def take_data():
            new_data=[]
            for i in range(1,10):
                new_data.append(entrys[i].get())
            new_data.append(about_text.get(1.0,END))
            arr=[new_data[2],new_data[3],new_data[4],new_data[5],new_data[8]]
            if entrys[0].get()!='ID задаётся базой данной':
                new_data.append(entrys[0].get())
            elif '' in arr:
                new_data[2]='0'
                new_data[3]='0'
                new_data[4]='0'
                new_data[5]='0'
                new_data[8]='0'
            new_data[2]=rplc(new_data[2])
            new_data[3]=rplc(new_data[3])
            new_data[8]=rplc(new_data[8])
            new_data[9]=new_data[9].replace('\n',' ')
            for i in range(len(new_data)):
                if 'null' in new_data[i]: new_data[i]=None
            return tuple(new_data)
        #обновление/вставка товара
        def update_item():
            sql='update items set name=%s,type=%s,volume=%s,alcohol=%s,year=%s,price=%s,country=%s,producer=%s,empty_weight=%s,about=%s where item_id=%s'#,str(entry[0])
            cursor.execute(sql,take_data())
            status.config(text=noow()+'Обновлены сведения товара с id='+entrys[0].get())
        def insert_item():
            sql='insert into items (name,type,volume,alcohol,year,price,country,producer,empty_weight,about) values '+str(take_data())
            cursor.execute(sql)
            status.config(text=noow()+'Добавлен новый товар')
        #очищает поля ввода
        def clear():
            for i in range(10):
                entrys[i].delete(0,END)
                entrys[i].insert(0,selected[i])
            about_text.delete(1.0, END)
            about_text.insert(1.0,selected[10])
        #возвращает данные, которые были изначально
        def reset():
            clear()
            update_item()
        name=Label(self, text='Информация о товаре')
        name.pack()
        status=Label(self,text='',font=("Arial", 12),anchor=W) #до 55 символов
        status.config(text='Ничего не произошло')
        status.pack(padx=0,pady=0,fill=X,side=BOTTOM)
        Frame(self, width=400, height=2, bg='white').pack()
        frame=Frame(self)
        frame.pack()
        for i in range(11):
            lt=['id',"Название","Категория","Объём","Алкоголь",'Год','Цена','Страна','Производитель','Вес тары','О товаре']
            Label(frame,text=lt[i]+':').grid(row=i+1,column=0,sticky=W)
            e=Entry(frame,width=22)
            e.grid(row=i+1,column=1,sticky=W)
            e.insert(0,selected[i])
            e.config(state='disable')
            entrys.append(e)
            b=Button(frame,width=30,text='✎',command=lambda a=i:edit(a))
            b.grid(row=i+1,column=2)
            buttons.append(b)
        b=Button(frame,width=50,text='✎ всё',bg='white')
        b.grid(row=0,column=2)
        b.config(command=editall)
        buttons.append(b)
        entrys[10].destroy()
        buttons[0].destroy()
        about_text=Text(frame,width=29,height=5,bg='#323232')
        about_text.insert(1.0,selected[10])
        about_text.config(state='disable',fg='#B1B2B1')
        about_text.grid(row=11,column=1,sticky=W)
        buttons[10].config(command=editabout)
        frame=Frame(self,bg='red')
        frame.pack()
        rst=Button(frame,width=170,text='Сбросить изменения',command=reset)
        rst.grid(row=0,column=0)
        commit=Button(frame,width=170,text='Применить изменения',command=update_item)
        commit.grid(row=0,column=1)
        if new==1:
            new_item()
        Button(self,text='Ок',command=exit).pack(pady=10,side=BOTTOM)
        self.wm_transient(container)
        self.resizable(False, False)
#класс дочернего окна (уведомление)
class WindowMessage(tk.Toplevel):
    def __init__(self, container, case):
        super().__init__(container)
        x=container.winfo_rootx()+25
        y=container.winfo_rooty()+20
        self.geometry('450x100+%s+%s'%(x,y))
        self.grab_set()
        self.overrideredirect(True)
        self.wm_transient(container)
        self.resizable(False, False)
        self.after(2000,lambda:self.destroy())
        label=Label(self, text='',font=('Microsoft YaHei UI Light', 24))
        label.place(relx=0.5,rely=0.5,anchor=CENTER)
        if case==1:
            label.config(text='Добро пожаловать!')
        elif case==2:
            label.config(text='Неправильный пароль.')
        elif case==3:
            label.config(text='Неправильный логин или пароль.')
#класс виджета с иконкой приложения
class FrameIcon(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.img=PhotoImage(file='images/bartender_icon.png')
        Label(self, image=self.img, bg=bgc).pack()
        self.pack(pady=50,side=TOP)
#класс виджета с главным меню приложения
class FrameMenu(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        def logout():
            container.destroy()
            FrameLogin(App()).pack()
        def ranframeitems():
            self.destroy()
            frame=FrameItems(container)
            container.title("Товары")
            frame.place(relx=0.5, y=0, anchor=N)
        def ranframeinventory():
            self.destroy()
            frame=FrameInventory(container)
            container.title("Инвентарь")
            frame.place(relx=0.5, y=0, anchor=N)
        def passs(): pass

        frame=Frame(self,width=460, height=400, bg=bgc)
        frame.pack(padx=0,pady=0)
        for i in range(5):
            c=[ranframeitems,ranframeinventory,passs,passs,passs]
            n=['Товары','Инвентарь','Настройки','Отчёты','Помощь']
            a=[30,90,150,210,270]
            Button(frame, width=200, text=n[i], bg=btc, border=0, font=('Microsoft YaHei UI Light', 28), fg='white', borderless=1, cursor="hand2",command=c[i]).place(relx=0.5, y=a[i], anchor=CENTER)
        logout=Button(frame, width=150, pady=7, text='Выйти', fg='white', bg='grey', borderless=1, cursor="hand2", command=logout)
        logout.place(relx=0.5, y=350, anchor=CENTER)
        self.pack(padx=0,pady=0)
#класс виджета для работы с инвентарём бара
class FrameInventory(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg=bgc)
        #выход в главное меню
        def doexit():
            self.destroy()
            status.destroy()
            FrameMenu(container)
        #заполнение таблицы
        def fill_table():
            for row in tree.get_children():
                tree.delete(row)
            counter_rows=0
            cursor.execute('select item_id,weight_left,amount from inventory')
            for i in cursor:
                if counter_rows%2==0:
                    tree.insert('',END,counter_rows,text="",values=(i[0],i[1],i[2]),tags=("lighter"))
                else:
                    tree.insert('',END,counter_rows,text="",values=(i[0],i[1],i[2]),tags=("darker"))
                counter_rows+=1
            status.config(text=noow()+'Таблица заполнена данными из базы данных.')
        #возвращает массив с информацией о выбранном товаре
        def info_of_selected(a):
            if a==None:
                a=tree.item(tree.selection())['values'][0]
            cursor.execute('select * from items where item_id='+str(a))
            arr=[]
            for i in cursor:
                for j in range(11):
                    arr.append(i[j])
            return arr
        #запускает дочернее окно с информацией о выбранном твоаре
        def info():
            if len(tree.selection())!=1:
                status.config(text=noow()+'Ошибка: Должна быть выбрана ОДНА строка для её удаления или справки')
                pass
            arr=info_of_selected(None)
            WindowInfo(self,arr,0)
            status.config(text=noow()+'Было открыто всплывающее окно. По его закрытии - обновите')
        #выводит в статус-бар соотношение остатка и объёма
        def ost_vol():
            if len(tree.selection())!=1:
                status.config(text=noow()+'Ошибка: Должна быть выбрана ОДНА строка для её удаления или справки')
                pass
            text=tree.item(tree.selection())['values'][1]
            vol=info_of_selected(None)[3]
            status.config(text=noow()+'Остаток составляет %s от %s'%(text,vol))
        #добавить новый товар в инвентарь
        def insert_ost():
            text_entrys=[]
            for i in range(len(entrys)):
                text_entrys.append(entrys[i].get())
            if info_of_selected(text_entrys[0])!=[]:
                if float(text_entrys[1])<=float(info_of_selected(text_entrys[0])[3]):
                    try:
                        cursor.execute('insert into inventory (item_id,weight_left,amount) values '+str(tuple(text_entrys)))
                        fill_table()
                        status.config(text=noow()+'Добавлен новый товар в инвентарь')
                    except sql.Error as err:
                        status.config(text=noow()+str(err))
                        if '1062' in status['text']:
                            cursor.execute('SET SQL_SAFE_UPDATES = 0')
                            cursor.execute('update inventory set amount=amount+%s where item_id=%s and weight_left=%s',(text_entrys[2],text_entrys[0],text_entrys[1]))
                            cursor.execute('SET SQL_SAFE_UPDATES = 1')
                            fill_table()
                            status.config(text=noow()+'Остаток совпал с другой строкой, увеличено количество')
                            pass
                else:
                    status.config(text=noow()+'Остаток не может быть больше объёма/текущего остатка! (Объём=%s)'%info_of_selected(text_entrys[0])[3])
            else:
                status.config(text=noow()+'Нет товара с id='+text_entrys[0])
        #изменить количество выбранного товара
        def change_amnt():
            if len(tree.selection())!=1:
                status.config(text=noow()+'Ошибка: Должна быть выбрана ОДНА строка для её удаления или справки')
                pass
            new_amnt=amnt.get()
            curamount=tree.item(tree.selection())['values'][2]
            itemid=tree.item(tree.selection())['values'][0]
            curost=tree.item(tree.selection())['values'][1]
            if new_amnt!=0:
                cursor.execute('update inventory set amount=%s where item_id=%s and weight_left=%s',(new_amnt,itemid,curost))
                fill_table()
            else: delete_it()
        #удалить выбранный товар из инвентаря
        def delete_it():
            if len(tree.selection())!=1:
                status.config(text=noow()+'Ошибка: Должна быть выбрана ОДНА строка для её удаления или справки')
                pass
            itemid=tree.item(tree.selection())['values'][0]
            curost=tree.item(tree.selection())['values'][1]
            cursor.execute('SET SQL_SAFE_UPDATES = 0')
            cursor.execute('delete from inventory where item_id=%s and weight_left=%s',(itemid,curost))
            cursor.execute('SET SQL_SAFE_UPDATES = 1')
            fill_table()
        #изменить остаток выбранного товара
        def change_ost():
            if len(tree.selection())!=1:
                status.config(text=noow()+'Ошибка: Должна быть выбрана ОДНА строка для её удаления или справки')
                pass
            itemid=tree.item(tree.selection())['values'][0]
            curost=tree.item(tree.selection())['values'][1]
            curamount=tree.item(tree.selection())['values'][2]
            vol=info_of_selected(None)[3]
            text=float(ost.get())
            if text<=vol and text<float(curost):
                try:
                    cursor.execute('update inventory set weight_left=%s where item_id=%s and weight_left=%s',(ost.get(),itemid,curost))
                    fill_table()
                    status.config(text=noow()+'Остаток обновлён для товара с id='+str(itemid))
                except sql.Error as err:
                    status.config(text=noow()+str(err))
                    if '1062' in status['text']:
                        cursor.execute('SET SQL_SAFE_UPDATES = 0')
                        cursor.execute('delete from inventory where item_id=%s and weight_left=%s',(itemid,curost))
                        cursor.execute('update inventory set amount=amount+%s where item_id=%s and weight_left=%s',(curamount,itemid,ost.get()))
                        cursor.execute('SET SQL_SAFE_UPDATES = 1')
                        fill_table()
                        status.config(text=noow()+'Остаток совпал с другой строкой, увеличено количество')
                    pass
            else:
                status.config(text=noow()+'Остаток не может быть больше объёма/текущего остатка! (Объём=%s)'%info_of_selected()[3])
        exit=Button(self, width=100, text='Назад', bg=btc, border=0, font=('Microsoft YaHei UI Light', 14), fg='white', borderless=1, cursor="hand2",command=doexit)
        exit.pack(padx=0,pady=3, anchor=NW)
        status=Label(container,text='',font=("Arial", 12),anchor=W) #до 55 символов
        status.config(text='Ничего не произошло')
        status.pack(padx=0,pady=0,fill=X,side=BOTTOM)
        frame_tree_scroll=Frame(self,bg=bgc)
        scrollbar=Scrollbar(frame_tree_scroll,orient=VERTICAL)
        tree=ttk.Treeview(frame_tree_scroll,yscrollcommand=scrollbar.set, selectmode=EXTENDED, show='headings', height=30)
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side=RIGHT,fill=Y)
        heads=["ID","Остаток","Количество"]
        tree["columns"] = heads
        for i in heads:
            tree.heading(i,text=i)
        for i in heads:
            tree.column(i,width=160)
        tree.tag_configure('lighter',background='#757575')
        tree.tag_configure('darker',background='#38393A')
        fill_table()
        tree.pack(padx=0,pady=0)
        frame_tree_scroll.pack()
        f=Frame(self)
        f.pack(padx=0,pady=0,fill=X)
        full_info=Button(f, width=200, text='Информация о товаре', bg=btc, border=0, font=('Microsoft YaHei UI Light', 14), fg='white', borderless=1, cursor="hand2",command=info)
        full_info.grid(row=0,column=0,columnspan=2,pady=10)
        ostvol=Button(f, width=150, text='Остаток/Объём', bg=btc, border=0, font=('Microsoft YaHei UI Light', 14), fg='white', borderless=1, cursor="hand2",command=ost_vol)
        ostvol.grid(row=0,column=2,columnspan=2,pady=10)
        dlt=Button(f, width=80, text='Удалить', bg=btc, border=0, font=('Microsoft YaHei UI Light', 14), fg='white', borderless=1, cursor="hand2",command=delete_it)
        dlt.grid(row=0,column=4,pady=10)
        ost_l=Label(f,text='Остаток',fg='white')
        ost_l.grid(row=1,column=0)
        ost=Entry(f,width=10)
        ost.grid(row=2,column=0)
        ost_b=Button(f, width=100, text='Изменить', bg=btc, border=0, font=('Microsoft YaHei UI Light', 14), fg='white', borderless=1, cursor="hand2",command=change_ost)
        ost_b.grid(row=3,column=0)
        amnt_l=Label(f,text='Количество',fg='white')
        amnt_l.grid(row=1,column=1)
        amnt=Entry(f,width=10)
        amnt.grid(row=2,column=1)
        amnt_b=Button(f, width=100, text='Изменить', bg=btc, border=0, font=('Microsoft YaHei UI Light', 14), fg='white', borderless=1, cursor="hand2",command=change_amnt)
        amnt_b.grid(row=3,column=1)
        entrys=[]
        for i in range(3):
            l=Label(f,text=heads[i])
            l.grid(row=1,column=i+2)
            e=Entry(f,width=10)
            e.grid(row=2,column=i+2)
            entrys.append(e)
        insrtost=Button(f, width=200, text='Добавить остаток', bg=btc, border=0, font=('Microsoft YaHei UI Light', 14), fg='white', borderless=1, cursor="hand2",command=insert_ost)
        insrtost.grid(row=3,column=2,columnspan=3,padx=50)
#класс виджета для работы с ассортиментом товаров бара
class FrameItems(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg=bgc)
        #выход в главное меню
        def doexit():
            self.destroy()
            status.destroy()
            FrameMenu(container)
        #удаление выбранного объекта
        def delete_item():
            slct_id=tree.item(tree.selection())['values'][4]
            cursor.execute('SET SQL_SAFE_UPDATES = 0')
            cursor.execute('delete from items where item_id='+str(slct_id))
            cursor.execute('SET SQL_SAFE_UPDATES = 1')
            fill_table('select name,type,volume,alcohol,item_id from items',None)
            status.config(text=noow()+'Удалён товар с id='+str(slct_id)+'. Таблица заполнена данными из базы данных.')
        #заполнение таблицы
        def fill_table(sql,tlp):
            for row in tree.get_children():
                tree.delete(row)
            counter_rows=0
            cursor.execute(sql,tlp)
            a=None
            for i in cursor:
                if counter_rows%2==0:
                    tree.insert('',END,counter_rows,text="",values=(i[0],i[1],str(i[2]),str(i[3]),str(i[4])),tags=("lighter"))
                else:
                    tree.insert('',END,counter_rows,text="",values=(i[0],i[1],str(i[2]),str(i[3]),str(i[4])),tags=("darker"))
                counter_rows+=1
                a=str(i[4])
            status.config(text=noow()+'Таблица заполнена данными из базы данных.')
            return a
        #возвращает массив информации о выбранном товаре
        def info_of_selected():
            a=tree.item(tree.selection())['values'][4]
            cursor.execute('select * from items where item_id='+str(a))
            arr=[]
            for i in cursor:
                for j in range(11):
                    arr.append(i[j])
            status.config(text=noow()+'Показаны сведения товара с id='+str(a))
            return arr
        #запускает дочернее окно с информацией о выбранном товаре
        def info():
            arr=info_of_selected()
            WindowInfo(self,arr,0)
            status.config(text=noow()+'Было открыто всплывающее окно. По его закрытии - обновите')
        #запускает дочернее окно для добавления нового товара
        def new_item_info():
            arr=['']*11
            WindowInfo(self,arr,1)
            status.config(text=noow()+'Было открыто всплывающее окно. По его закрытии - обновите')
        #осуществляет поиск по таблице
        def search():
            tlp=('%'+search_e.get()+'%',)*10
            sql='select name,type,volume,alcohol,item_id from items where name like %s or type like %s or volume like %s or alcohol like %s or year like %s or price like %s or country like %s or producer like %s or empty_weight like %s or about like %s'
            fill_table(sql,tlp)
            status.config(text=noow()+'Результаты поиска по запросу "%s"'%search_e.get())
        #проверяет выбрана ли одна и только одна строка
        def check_selection(function):
            if len(tree.selection())!=1: status.config(text=noow()+'Ошибка: Должна быть выбрана ОДНА строка для её удаления или справки')
            else:
                function()
        #устанавливает команду на кнопку через проверку строки
        def set_command(this_button,com):
            this_button.config(command=lambda a=com:check_selection(a))
        #кнопка выхода в главное меню
        frame_top=Frame(self,bg=bgc)
        frame_top.pack(padx=0,pady=4,fill=X,side=TOP)
        exit=Button(frame_top, width=100, text='Назад', bg=btc, border=0, font=('Microsoft YaHei UI Light', 14), fg='white', borderless=1, cursor="hand2",command=doexit)
        exit.grid(row=0,column=0,sticky=W)
        Label(frame_top,width=20,bg=bgc).grid(row=0,column=1)
        search_e=Entry(frame_top,border=0, highlightthickness=0)
        search_e.grid(row=0,column=2,sticky=E)
        search_b=Button(frame_top,width=30,text='🔍',bg=btc,border=0,borderless=1,font=('Arial',10),command=search)
        search_b.grid(row=0,column=3,sticky=W)
        status=Label(container,text='',font=("Arial", 12),anchor=W) #до 55 символов
        status.config(text='Ничего не произошло')
        status.pack(padx=0,pady=0,fill=X,side=BOTTOM)
        #фрейм таблицы и её скроллбара
        frame_tree_scroll=Frame(self,bg=bgc)
        scrollbar=Scrollbar(frame_tree_scroll,orient=VERTICAL)
        tree=ttk.Treeview(frame_tree_scroll,yscrollcommand=scrollbar.set, selectmode=EXTENDED, show='headings', height=30)
        scrollbar.config(command=tree.yview)
        scrollbar.pack(side=RIGHT,fill=Y)
        heads=["Название","Категория","Объём","Алкоголь","ID"]
        tree["columns"] = heads
        for i in heads:
            tree.heading(i,text=i)
        for i in heads:
            tree.column(i,width=60)
        tree.column(heads[0],width=210)
        tree.column(heads[1],width=150)
        tree.column(heads[4],width=0,stretch=0)
        tree.tag_configure('lighter',background='#757575')
        tree.tag_configure('darker',background='#38393A')
        tree.pack(padx=0,pady=0)
        frame_buttons=Frame(self,bg=bgc)
        buttons=[]
        for i in range(4):
            w=[80,200,85,85]
            n=['Удалить','Посмотреть информацию','Обновить','Добавить']
            c=[delete_item,info,lambda a='select name,type,volume,alcohol,item_id from items':fill_table(a,None),new_item_info]
            p=[2,2,10,10]
            b=Button(frame_buttons, width=w[i], text=n[i], bg=btc, border=0, font=('Microsoft YaHei UI Light', 14), fg='white', borderless=1, cursor="hand2",command=c[i])
            b.grid(row=0,column=i,padx=p[i])
            if i==0 or i==1:
                set_command(b,c[i])
            buttons.append(b)
        fill_table('select name,type,volume,alcohol,item_id from items',None)
        frame_tree_scroll.pack(padx=0,pady=0)
        Frame(self, width=550, height=5, bg='Black').pack()
        frame_buttons.pack(padx=0,pady=10)
        self.place(x=0,y=0)
#класс виджета с копирайтом
class FrameCopyright(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        copyright=Label(self, text="Версия 1.0", fg="#808080", bg=bgc, font=('Microsoft YaHei UI Light', 14)) #bg=bgc
        copyright.pack(padx=0,pady=0)
        self.pack(pady=10,side=BOTTOM)
#класс виджета авторизации
class FrameLogin(tk.Frame):
    def __init__(self, container):
        super().__init__(container,bg=bgc)
        #обработка логина и пароля
        def login():
            query_get_login_pswrd='SELECT login,password FROM users'
            cursor.execute(query_get_login_pswrd)
            counter=0
            users_num=0
            passwords=[]
            logins=[]
            for i in cursor:
                for j in i:
                    if counter%2 == 0:
                        logins.append(j)
                    else:
                        passwords.append(j)
                    counter += 1
            username=user.get()
            password=psword.get()
            for i in range(len(logins)):
                if logins[i]==username and passwords[i]==password:
                    cprt.destroy()
                    self.destroy()
                    FrameIcon(container)
                    FrameMenu(container)
                    WindowMessage(container,1)
                elif username in logins:
                    psword.delete(0, END)
                    psword.insert(0, 'Пароль')
                    WindowMessage(container,2)
                else:
                    user.delete(0, END)
                    user.insert(0, 'Логин')
                    psword.delete(0, END)
                    psword.insert(0, 'Пароль')
                    WindowMessage(container,3)
        #обработка событий полей ввода
        def in_user(e):
            if user.get()=="Логин":
                user.delete(0, END)
        def in_pswrd(e):
            if psword.get()=="Пароль":
                psword.delete(0, END)
        def out_entry(e):
            if psword.get()=="":
                psword.insert (0, 'Пароль')
            elif user.get()=="":
                user.insert (0, 'Логин')
        FrameIcon(self)
        Label(self, text='Войдите в аккаунт', fg='white', bg=bgc, font=('Microsoft YaHei UI Light', 23, 'bold')).pack(pady=10)

        user=Entry(self, width=30, fg='white', border=0, highlightthickness=0, bg=bgc, font=('Microsoft YaHei UI Light', 14))
        user.pack(pady=10)
        user.insert(0, 'admin')
        Frame(self, width=285, height=2, bg='white').pack()
        user.bind('<FocusIn>', in_user)
        user.bind('<FocusOut>', out_entry)

        psword=Entry(self, width=30, fg='white', border=0, highlightthickness=0, bg=bgc, font=('Microsoft YaHei UI Light', 14))
        psword.pack(pady=10)
        psword.insert(0, '123')
        Frame(self, width=285, height=2, bg='white').pack()
        psword.bind('<FocusIn>', in_pswrd)
        psword.bind('<FocusOut>', out_entry)

        go=Button(self, width=200, pady=7, text='Войти', fg='white', bg='grey', borderless=1, command=login, cursor="hand2")
        go.pack(pady=40)
        frame=Frame(self,bg=bgc)
        frame.pack(pady=0)
        signup=Label(frame, text="Зарегистироваться", fg='white', bg=bgc, font=('Microsoft YaHei UI Light' ,12))
        signup.grid(row=0,column=0,padx=5)
        forgotpsword=Label(frame, text="Забыли пароль?", fg='white', bg=bgc, font=('Microsoft YaHei UI Light' ,12))
        forgotpsword.grid(row=0,column=1,padx=5)
        self.pack(padx=0,pady=0)
        cprt=FrameCopyright(container)
#класс создания контейнера
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Авторизация в Bartender")
        self.geometry("500x750+1100+100")
        self.config(bg=bgc)
        self.resizable(False, False)

if __name__ == "__main__":
    app=App()
    FrameLogin(app).pack()
    app.mainloop()
