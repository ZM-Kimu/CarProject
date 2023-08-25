getTicksLastFrame=0
        radius=self.MusicVisual.radius
        poly_color=self.MusicVisual.poly_color
        bass_trigger=self.MusicVisual.bass_trigger
        polygon_default_color=self.MusicVisual.polygon_default_color
        polygon_bass_color=self.MusicVisual.polygon_bass_color
        polygon_color_vel=self.MusicVisual.polygon_color_vel
        bass_trigger_started=self.MusicVisual.bass_trigger_started

        min_radius=self.MusicVisual.min_radius
        max_radius=self.MusicVisual.max_radius
        min_decibel=self.MusicVisual.min_decibel
        max_decibel=self.MusicVisual.max_decibel

        self.MusicVisual.MainAnalyze(self.Music.FolderPath+"/"+self.Music.MusicList[self.MusicNow])

        running = True
        while running:

            avg_bass = 0
            self.MusicVisual.poly = []

            t = mixer.music.get_pos()
            deltaTime = (t - getTicksLastFrame) / 1000.0
            getTicksLastFrame = t

            if mixer.music.get_busy() == False:
                running = False

            for b1 in self.MusicVisual.bars:
                for b in b1:
                    b.update_all(
                        deltaTime, mixer.music.get_pos() / 1000.0, self.MusicVisual.analyzer)

            #b为bars内的第一个实例，即低音频率类，由于self.avg已经由上方的update_all方法改变，因此在时间点是有效的
            for b in self.MusicVisual.bars[0]:
                avg_bass += b.avg#获取在某时间点下的低音频率类的平均分贝

            avg_bass /= len(self.MusicVisual.bars[0])#将低音频率类的值归细

            if avg_bass > bass_trigger:
                #以下代码块控制在低音触发下的图形的整体缩放
                if bass_trigger_started == 0:
                    bass_trigger_started = mixer.music.get_pos()#得到低音时的时间
                if (mixer.music.get_pos() - bass_trigger_started)/1000.0 > 2:#（例外情况）
                    polygon_bass_color = rnd_color()
                    bass_trigger_started = 0
                if polygon_bass_color is None:#（例外情况）
                    polygon_bass_color = rnd_color()
                #将分贝范围与圆范围进行匹配，并得出经过低音振幅大小后的新直径
                newr = min_radius + int(avg_bass * ((max_radius - min_radius) /
                                        (max_decibel - min_decibel)) + (max_radius - min_radius))
                #半径需要移动的距离的宏观化
                radius_vel = (newr - radius) / 0.15
                #在低音触发后淡出时的颜色改变
                polygon_color_vel = [
                    (polygon_bass_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]
            #当不处于低音触发时，如果现在的图形状态大于默认状态；即控制低音触发后进行动画收回的代码块
            elif radius > min_radius:
                bass_trigger_started = 0
                polygon_bass_color = None
                radius_vel = (self.MusicVisual.min_radius - radius) / 0.15
                polygon_color_vel = [
                    (polygon_default_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]
            #在未被低音触发或从触发恢复的正常态下，图形大小保持默认值
            else:
                bass_trigger_started = 0
                poly_color = polygon_default_color.copy()
                polygon_bass_color = None
                polygon_color_vel = [0, 0, 0]

                radius_vel = 0
                radius = min_radius

            #在每次循环加上半径变化值乘上时间状态经过的值，有助于非线性变化
            radius += radius_vel * deltaTime

            #用以处理颜色渐变
            for x in range(len(polygon_color_vel)):
                value = polygon_color_vel[x]*deltaTime + poly_color[x]
                poly_color[x] = value

            #获取在bars内每个实例对象的x与y的坐标
            for b1 in self.MusicVisual.bars:
                for b in b1:
                    #可通过调参更改柱状的倾角
                    b.x, b.y = self.MusicVisual.circleX+radius * math.cos(math.radians(b.angle - 200)), self.MusicVisual.circleY + radius * math.sin(math.radians(b.angle - 200))
                    b.update_rect()

                    #在此append方法中，poly只关心目标坐标，即柱状高度
                    self.MusicVisual.poly.append(b.rect.points[3])
                    self.MusicVisual.poly.append(b.rect.points[2])

            canvas.delete("all")
            canvas.create_polygon(self.MusicVisual.poly,fill=rgb2hex(poly_color))
            canvas.create_oval(screen_w/2-int(radius)/1.5+5,screen_h/2-int(radius)/1.5,screen_w/2+int(radius)/1.5+5,screen_h/2+int(radius)/1.5,fill=rgb2hex(self.MusicVisual.circle_color))