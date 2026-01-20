from app.navegador import Navegador
from .manage_db import mudar_profile, profile_tiktok
from .functions import carregar_fernet
from .logger import log, chat_dialog
import  asyncio
from random import randint, uniform
from nodriver import Element, Tab
from datetime import datetime



class System:
    def __init__(self):
        self.navegador = None
        self.nav: Navegador = None
        self.nav_ligada: bool = False
        self.lista_profiles_cadastrados: list = []
        self.change_title = None
        self.get_like: Tab = None
        self.tiktok: Tab = None
        self.sad_captcha: Tab = None
        self.profile: str = None
        self.total_like: int = 0
        self.block_like: int = 0
        self.email_getlike = "v.arpinheiro3@gmail.com"
        self.senha_getlike = "varp2607"
        
        
    # @classmethod    
    # async def create_system(create):
    #     self = create()
    #     await self.set_tabs()
    #     await self.start_navegador()
        
        
    async def start_navegador(self):
        self.nav = Navegador()
        #self.nav._backup()
        await self.nav.restore()
        self.navegador = await self.nav.iniciar()
        await asyncio.sleep(3)
        self.nav_ligada = True
        self.profile = self.nav.profile
        self.total_like = 0
        log(f"Starting Navegador com Profile: {self.profile}")     
        return self.nav
    
    
    async def start_nav(self):
        self.navegador = Navegador()
        await self.navegador.init()
        self.nav = self.navegador.nav
        self.nav_ligada = True
        self.profile = self.navegador.profile
        self.total_like = 0
        log(f"Starting Navegador com Profile: {self.profile}")     
        return self.nav


    async def stop(self):
        if self.nav_ligada:
            return await self.navegador.stop()
        

    async def mostrar_navegador(self):
        if self.nav_ligada:
            return await self.nav.show_browser()
        else:
            log(f"❌ Navegador Ainda não foi iniciado")
            return False
        
        
    async def set_tab_tiktok(self):
        if not self.nav_ligada:
            await self.start_navegador()
        link_tiktok = "https://www.tiktok.com/"
        self.tiktok = await self.nav.get(link_tiktok, new_tab=True)
        return self.tiktok
    
        
    async def set_tab_getlike(self):
        link_getlike = "https://getlike.io/en/tasks/tiktok/like/"
        self.get_like = await self.nav.get(link_getlike)
        return self.get_like
        

    async def logged_in_to_getlike(self):
        try:
            # logado = await self.get_like.query_selector(f'span[data-original-title="{self.email_getlike}"]')
            logado = await self.get_like.evaluate("document.querySelector('h3[title=\"v.arpinheiro3\"]').title")
            accont_get_like = "v.arpinheiro3"
            return bool(accont_get_like in logado)
        except Exception as erro:
            log(f"Deu Ruim Profile ñ esta logado!\nErro: {erro}")  


    async def profiles_cadastrados(self):
        profiles = await self.get_like.select_all('.media-link.text-capitalize')
        lista = [profile.text for profile in profiles]
        for i, perfil in enumerate(lista):
            if i % 2 == 0:
                pass
            else:
                self.lista_profiles_cadastrados.append(perfil.lower().strip())
        return self.lista_profiles_cadastrados
    
    
    async def continuar(self):
        try:
            self.nav.stop()
            await asyncio.sleep(randint(3,6))
            # await self.nav.matar_chromium()
            # await asyncio.sleep(randint(3,6))
            self.nav._backup()
        except Exception as error:
            log(f"Erro: {error}")
        finally:
            from app import app
            self.nav_ligada = False
            self.block_like = 0
            self.total_like = 0
            next_profile = mudar_profile()
            self.profile = next_profile
            if next_profile in self.lista_profiles_cadastrados:
                app.detectar_perfil()
                log(f"Mudança para o Porfile: {next_profile} Efetuada com Sucess")
                await asyncio.sleep(3)
                log(f"Trabalhando com o Profile: {self.profile}")
                return next_profile              
            return await self.continuar()
    
      
    
    async def selection_profile(self):
        try:
            await self.get_like.evaluate("window.confirm = () => true;")
            profile_current = await self.get_like.query_selector(".media-info-name.text-capitalize.text-overflow")
            profile_current = profile_current.text.lower().strip()
            if profile_current == self.profile:
                log(f"Profile: {self.profile} ja está Selecionado")
                return self.profile 
            else:
                log(f"Mudando para o Profile: {self.profile}")
                profiles = await self.get_like.query_selector_all('li.media.media_table.media_default.media_padding-adp.media_md.js-app-user-social-block')
                switch = await self.get_like.query_selector('[title=\"Switch account\"]')
                await switch.click()
            for perfil in profiles:
                perfil : Element = perfil
                text_perfil = await perfil.query_selector('span.media-link.text-capitalize')
                text_profile = text_perfil.text.lower().strip() 
                if self.profile == text_profile:
                    log(f"Profile Encontrado: {text_profile}")
                    button = await perfil.query_selector("div.label.label-primary.label_block.label-light.js-app-choose-user-social-current-label")
                    if button:
                        await button.click()
                        await asyncio.sleep(3)
                    break
            await self.get_like.reload()
            await asyncio.sleep(3)
        except Exception as erro:
            log(f"Não foi possivel mudar para o Profile: {self.profile}...Vamos tentar Novamente")
            await self.get_like.reload()
            await asyncio.sleep(3)
            return await self.selection_profile()
        text_profile: Element = await self.get_like.query_selector('.media-info-name.text-capitalize.text-overflow')
        profile_atual = text_profile.text.lower().strip()
        if profile_atual == self.profile:
            log(f"Mudança para o Profile: {self.profile} Efetuada com Sucess")
            return self.profile
        else:
            log(f"Não foi possivel mudar para o Profile: {self.profile}...Vamos tentar Novamente")
            await self.get_like.reload()
            await asyncio.sleep(3)
            return await self.selection_profile()  
        
        
        
    async def unlock_tasks(self):
        box_tasks: Element = await self.get_like.query_selector('div[class=\"js-tpl-tasks-list\"]')
        tiktok_tasks = await box_tasks.query_selector_all("article") 
        for task in tiktok_tasks:
            task: Element
            btn = await task.query_selector('.do.do-task-m.btn.btn-sm.btn-primary.btn-block')
            await btn.click()
        return box_tasks


    async def get_tasks(self):
        list_links = []
        links = await self.get_like.query_selector_all('a[class*="goto-task btn-info btn btn-sm btn-block m-t-0"]')
        log("Lista de Tasks do Tiktok:")
        for link in links:
            link: Element
            list_links.append(link.attributes[3])
            log(f"Link: {link.attributes[3]}")
        return list_links


    async def mute(self):
        try:
            script = """
                const elementos = document.querySelectorAll('video, audio');
                elementos.forEach(elemento => elemento.muted=true);
            """
            await self.tiktok.evaluate(script)
            log("Consegui Tirar o Som")
            # elementos = await tiktok.query_selector_all('video, audio')
            # for elemento in elementos:
            #     elemento: Element
            #     await elemento.apply("this.volume = 0; this.muted = true;")
            return self.tiktok
        except Exception as erro:
            log(f"Não possivel mutar o Som")
            log(f"Erro: {erro}")
            return False


    async def captcha(self):
        try:
            modal = await self.tiktok.query_selector('div.TUXModal.captcha-verify-container')
            # captcha = await tiktok.evaluate("document.getElementById('captcha_slide_button')")
            if modal:
                log("Captcha Detectado")
                await asyncio.sleep(randint(6,9))
                # slide: Element = await tiktok.query_selector('#captcha_slide_button')
                # pos_slide = await slide.get_position()
                # await tiktok.mouse_drag(pos_slide[0], pos_slide[1])
                
                # await resolver_captcha_slide(tiktok)
                # tiktok.evaluate("document.querySelector('button[aria-label=\"Fechar\"]').click()")
                # tiktok.evaluate("return document.querySelector('[data-e2e=\"like-icon\"]').click()")
                # tiktok.reload()
                # if await curtido():
                #     log(f"{user_name} Já foi Curtido com Sucesso")
                #     total += 1
                #     log(f"{total} Ações Realizadas com Sucesso")
                #     log(f"{total} Ações Realizadas com Sucesso")
        except Exception as erro:
            log(f"Deu erro no Captcha: {erro}")


    async def logado(self):
        try:
            element_profile_logado: Element = await self.tiktok.query_selector('a[data-e2e=\"nav-profile\"]')
            element_perfil_logado: Element = await self.tiktok.query_selector('a[data-e2e="profile-icon"]')
            # for attr in element_profile_logado.attributes:
            #     if "@" in attr:      
            #         profile_logado = attr.strip()
            # profile_logado = profile_logado[24:].split('?')[0].strip()
            # log(profile_logado)
            if element_profile_logado or element_perfil_logado:
                # log(f"Esse é o Profile que esta logado: {profile_logado}")
                return True
        except Exception as erro:
            log(f"Falha ao Verificar login: {erro}")
            return False
            
        

    async def like_count(self):
        texto: Element = await self.tiktok.query_selector('strong[data-e2e=\"like-count\"]')
        like_count = texto.text.lower().replace("k", "")
        return int(float(like_count) * 1000)


    async def curtido(self):
        try:
            # script = """
            # (() => {
            #     const like = document.querySelector('button[class*="--ButtonActionItem"]');
            #     let pressed = like.getAttribute('aria-pressed');
            #     return pressed
            # })();
            # """
            # script = """
            #     (() => {
            #         const el = document.querySelector('span[data-e2e="like-icon"]');
            #          return el?.parentElement?.getAttribute("aria-pressed") === "true";
            #     })()
            # """ 
            curtido1 = await self.tiktok.query_selector('filter[id=\"LikeRedShadowColor_filter0_d\"]')
            curtido2 = await self.tiktok.query_selector('path[fill=\"rgb(254,44,85)\"]')
            curtido3 = await self.tiktok.query_selector('g[filter=\"url(#LikeRedShadowColor_filter0_d)\"]')
            if curtido1 or curtido2 or curtido3:
                return True
        except Exception as erro:
            log(f"Não Consegui Verificar o Like")
            return False


    async def check_tasks(self):
        check_task = await self.get_like.query_selector_all('a.check-task')
        for task in check_task:
            log("Entrei no for do Check tasks")
            task: Element
            await task.click()


    async def login_profile(self):
        if not self.nav_ligada:
            await self.start_navegador()
            await self.set_tab_tiktok()
        fernet = carregar_fernet()
        dados = profile_tiktok()
        username = dados[0]
        senha = fernet.decrypt(dados[1]).decode("utf-8")
        tiktok_login = "https://www.tiktok.com/login/phone-or-email/email"
        await self.tiktok.get(tiktok_login)
        if await self.logado():
            log(f"{self.profile} Logado com Sucesso")
            return True
        for _ in range(1,4):
            try:
                await self.tiktok.evaluate("document.querySelector('button[data-e2e=\"login-button\"]').removeAttribute('disabled')")
                
                input_username: Element = await self.tiktok.query_selector('input[placeholder=\"E-mail ou nome de usuário\"]')
                input_senha: Element = await self.tiktok.query_selector('input[placeholder=\"Senha\"]')
                
                await input_username.send_keys(username)
                # await input_username.apply(f"(username)=>document.querySelector('input[placeholder=\"E-mail ou nome de usuário\"]').value='{username}'")
                await asyncio.sleep(randint(1,2))
                await input_senha.send_keys(senha)
                # await input_senha.apply(f"(senha)=>document.querySelector('input[placeholder=\"Senha\"]').value='{senha}'")
                
                
                await self.tiktok.evaluate("document.querySelector('button[data-e2e=\"login-button\"]').click()")
                
                await asyncio.sleep(randint(9,12))
                # captcha = await tiktok.find('button[id="captcha_slide_button"]')
                # if captcha:
                #     input("Vc ja resolveu o captcha? e fez o Login: ")
                    
                if await self.logado():
                    log(f"{self.profile} Logado com Sucesso")
                    return True
                else:
                    log("Não foi Possivel fazer Login")
                    await self.tiktok.reload()
                    await asyncio.sleep(3)
                    continue
            except:
                await asyncio.sleep(randint(3, 6))
            
            if await self.logado():
                log(f"{self.profile} Logado com Sucesso")
                return True
            else:
                log("Tentei Entrar e não Consegui")
                await asyncio.sleep(randint(2,4))
        with open("logged_out.log", "a", encoding="utf-8") as logged_out:
            logged_out.write(f"Profile: {self.profile} esta Deslogado ==> {datetime.now()}\n")
        await asyncio.sleep(randint(1,2))
        await self.tiktok.close()
        return await self.continuar()

        
    async def login_getlike(self):
        if not self.nav_ligada:
            await self.start_navegador()
        await self.set_tab_getlike()
        await asyncio.sleep(randint(3,6))
        if await self.logged_in_to_getlike():
            log("Ja estamos Logados no site GetLike")
            return True
        await self.get_like.get("https://getlike.io/en/login/")
        await asyncio.sleep(randint(3,6))
        conta: Element = await self.get_like.query_selector('#User_loginLogin')
        text_conta: Element = await self.get_like.evaluate("document.getElementById('User_loginLogin').value")
        if text_conta == "":
            await conta.send_keys("v.arpinheiro3@gmail.com")
    
        await asyncio.sleep(randint(2,4))
    
        password: Element = await self.get_like.query_selector('#User_passwordLogin')
        text_password: Element = await self.get_like.evaluate("document.getElementById('User_passwordLogin').value")
        if text_password == "":
            await password.send_keys("varp2607")
        
        await asyncio.sleep(3)
        
        # iframe = await self.get_like.query_selector('iframe[title="reCAPTCHA"]')
        # check = await iframe.query_selector('.recaptcha-checkbox-checkmark')
        # await check.click()
        
        # await reCAPTCHA.apply('document.getElementById(rc-anchor-container).click()')
        # await self.get_like.evaluate("document.querySelector('#rc-anchor-container').click()")
        # pos = await check_captcha.get_position(abs=True)
        # x = pos.abs_x
        # y = pos.abs_y
        # self.get_like.mouse_move(x=x, y=y)
        # await self.get_like.mouse_click()
        
        # iframe = await self.get_like.query_selector('iframe[title="recaptcha challenge expires in two minutes"]')
        # check = await iframe.query_selector('span[id="recaptcha-anchor"]')
        # await check.click()
        
        """
        document.querySelector('iframe[title="recaptcha challenge expires in two minutes"]')
        document.querySelector('span[id="recaptcha-anchor"]')
        document.querySelector('#RecaptchaField1 div div')
        document.querySelector('.recaptcha-checkbox-checkmark').click()
        """
        
    
        log("⚠️ Faça login manualmente e resolva o CAPTCHA.")
        log('Voce já fez o login no site GetLikes ?')
        log("✅ Digite a palavra 'Ok' aqui quando o login estiver completo: ")
        ok = chat_dialog()
        while True:
            if await self.logged_in_to_getlike() or ok == "ok":
                return log('Salvando o seu login...')
            else:
                log("✅ Digite a palavra 'Ok' aqui quando o login estiver completo: ")



    async def simulation(self, link=None):
        try:
            user_video = link[23:]
            user_video = user_video.strip()
            log(user_video)
            user_name = user_video.split('/')[0]
            log(user_name)
            link = f"https://www.tiktok.com/{user_name}"
            log(link)
            await self.tiktok.get(link)
            await asyncio.sleep(randint(9,12))
            div_videos = await self.tiktok.query_selector('div[id="user-post-item-list"]')
            video = await self.tiktok.query_selector('div video[crossorigin="use-credentials"]')
            #videos: Element = await div_videos.query_selector_all('div[id*="grid-item-container"]')
            await asyncio.sleep(1)  
            await video.click()
            await asyncio.sleep(1)
            
            async def cont_temp():
                try:
                    tempo = await self.tiktok.query_selector('div[class*="DivSeekBarTimeContainer"]')
                    tempo = tempo.text.strip()
                    log(tempo)
                    temp1 = tempo.split("/")[0].strip()
                    #log(temp1)
                    temp2 = tempo.split("/")[1].strip()
                    temp2 = temp2.split(":")[1].strip()
                    temp2 = int(temp2)
                    if temp2 > 30:
                        return await asyncio.sleep(30)
                    await asyncio.sleep(temp2)
                except Exception as error:
                    log(f"Erro: {error}")
                    
            await cont_temp()
            button = await self.tiktok.query_selector('button[data-e2e="arrow-right"]')
            await button.click()
            await asyncio.sleep(1)
            await cont_temp()
            
            # link = "https://www.tiktok.com/"
            # await self.tiktok.get(link)
            # await asyncio.sleep(randint(3,6))
            # app = await self.tiktok.query_selector('div[id="app"]')
            # for i in range(3):
            #     video: Element = await app.query_selector(f'article[data-scroll-index="{i}"]')
            #     await video.scroll_into_view()
            #     if i >= 1:
            #         log(f"Rolei a página até o próximo vídeo...")
            #     await asyncio.sleep(randint(9,12))
        except Exception as erro:
            log(f"Erro: {erro}")




    async def click_like(self, user_name):
        try:
            #curtir = await self.tiktok.query_selector('span[data-e2e=\"like-icon\"]')
            # pos_curtir_span = await curtir.get_position(abs=True)
            # x_curtir = pos_curtir_span.abs_x
            # y_curtir = pos_curtir_span.abs_y
            #svg = await self.tiktok.query_selector("svg[data-e2e]")
            #section_like = await self.tiktok.query_selector('section[class*="SectionActionBarContainer"]')
            #button_like = await self.tiktok.query_selector('button[aria-label*="Curtir vídeo"]')
            button_like = await self.tiktok.query_selector('span[data-e2e="like-icon"]')
            div_like = await self.tiktok.query_selector('div[data-e2e="like-icon"]')
            if button_like:
                pos_curtir = await button_like.get_position(abs=True)
                x = pos_curtir.x + (pos_curtir.width/2)
                y = pos_curtir.y + (pos_curtir.height/2)
            if div_like:
                pos_curtir = await div_like.get_position(abs=True)
                x = pos_curtir.x + (pos_curtir.width/2)
                y = pos_curtir.y + (pos_curtir.height/2)
            x_init = randint(500, 700)
            y_init = randint(100, 300)
            x_alvo = x + randint(-3, 3)
            y_alvo = x + randint(-3, 3)
            # for _ in range(randint(2,4)):
            #     await tiktok.mouse_move(x + randint(-3, 3), y + randint(-3,3))
            #     await asyncio.sleep(uniform(0.1, 0.3))
            
            
            await self.tiktok.mouse_move(x=x_init, y=y_init, steps=randint(3,6))
            await asyncio.sleep(uniform(0.1, 0.3))
            
            await self.tiktok.mouse_move(x=x_alvo, y=y_alvo, steps=randint(60,120))
            await asyncio.sleep(uniform(0.3, 0.9))
            
            
            
            #await button_like.focus()
            #await asyncio.sleep(uniform(0.1, 0.3))
            # await self.tiktok.mouse_move(x= x_curtir+randint(-5,5), y= y_curtir+randint(-5,5))
            # await asyncio.sleep(uniform(0.1, 0.3))
            
            
            await self.tiktok.mouse_move(x= x, y= y, steps=randint(60,120))
            await asyncio.sleep(uniform(0.1, 0.3))
            
            # await self.tiktok.mouse_move(x=x_curtir, y=y_curtir)
            # await asyncio.sleep(uniform(0.1, 0.3))
            # await curtir.mouse_move()
            # await asyncio.sleep(uniform(0.1, 0.3))
            
            await button_like.mouse_move()
            await asyncio.sleep(uniform(0.1, 0.3))
            
            await button_like.scroll_into_view()
            await asyncio.sleep(uniform(0.1, 0.3))
            
            await self.tiktok.mouse_click(x=x, y=y)
            #await button_like.mouse_click()
            log(f"Cliquei no Coração Curtir com Mouse_Click")
            await asyncio.sleep(randint(2,4))
        except Exception as erro:
            log(f"Erro ao Tentar Curtir {user_name}")
            log(f"Error: {erro}")
        finally:
            await self.tiktok.reload()
            await asyncio.sleep(randint(2, 4))



    async def close_keyboard(self):
        try:
            # tiktok.evaluate("document.querySelector('div.css-hbdz7w-0be0dc34--DivXMarkWrapper.e1jppm6i4').click()")
            button_key = await self.tiktok.query_selector('div[class*="--DivXMarkWrapper"]')
            if button_key:
                await button_key.click()
                log(f"Button Keyboard clicado com Sucess")
        except Exception as erro:
            log(f"Keyboard ja foi Fechado Anteriormente!")
        


    async def like(self):
        if not self.nav_ligada:
            await self.start_navegador()
        log("Abrindo Site GetLikes")
        
        # url_get_like = "https://getlike.io/en/tasks/tiktok/like/"
        # self.get_like = await self.nav.get(url_get_like)
        await self.set_tab_getlike()
        await self.get_like.evaluate("window.confirm = () => true;")
            
        await asyncio.sleep(randint(3,6))
        
        if await self.logged_in_to_getlike():      
            await self.profiles_cadastrados()
            log(f"Lista de Profiles Cadastrados: {self.lista_profiles_cadastrados}")
        else:
            log("Get_Like esta Deslogado")         
            log("Vamos mudar para outro Profile")   
            return await self.continuar()
        
        await self.selection_profile()
        await asyncio.sleep(randint(1, 2))
        
        box_tasks: Element = await self.get_like.query_selector('div[class=\"js-tpl-tasks-list\"]')
        tiktok_tasks = await box_tasks.query_selector_all("article")
        
        if len(tiktok_tasks) == 0:
            log("No momento estamos sem Ações! Vamos Trocar para outro Perfil")
            await asyncio.sleep(randint(2,4))
            return await self.continuar()
        
        await asyncio.sleep(randint(2,4))

        await self.unlock_tasks()
        
        await asyncio.sleep(randint(2,4))
        
        list_links = await self.get_tasks()
        
        if len(list_links) == 0:
            log(f"{len(list_links)} perfils disponiveis para as Ações de Curtir")
            log("Executando Profile Change...")
            return await self.continuar()
        log(f"{len(list_links)} perfils disponiveis para as Ações de Curtir")
        
        while list_links:
            await self.set_tab_tiktok()
            await asyncio.sleep(randint(3,6))
            #await self.simulation(link=list_links[0])
            # await self.limpar_identidade_tiktok()
            # await self.set_sad_captcha()  
            for link in list_links:
                await self.simulation(link=link)
                #await asyncio.sleep(randint(10,30))
                await asyncio.sleep(randint(2,4))
                try:
                    await self.tiktok.get(link)
                    await asyncio.sleep(7)
                    
                    if await self.logado():
                        # log("Estamos Logados no Tiktok")
                        pass
                    else:
                        log("Profile Deslogado...Vamos Tentar fazer o Login")
                        await self.login_profile()
                        continue
                      
                    video = await self.tiktok.query_selector(".xgplayer-container.tiktok-web-player")
                    await video.click()
                    await asyncio.sleep(3)
                    
                    user_name = link[23:]
                    user_name = user_name.strip()
                    log(f"Abrimos {user_name} para Curtir")
                    
                    # like = await like_count(tiktok)
                            
                    
                    if await self.curtido():
                        log(f"{user_name} Já foi Curtido com Sucesso")
                        self.total_like += 1
                        log(f"{self.total_like} Ações Realizadas com Sucesso")
                        continue
                    
                    
                    if await self.captcha():
                        await asyncio.sleep(randint(2, 4))
    
                    if await self.close_keyboard():
                        await asyncio.sleep(randint(2, 4))
                    
                    await self.click_like(user_name)
                    await asyncio.sleep(randint(2, 4))
                    
                    if await self.curtido():
                        self.total_like += 1
                        log(f"{self.total_like} Ações Realizadas com Sucesso")
                        await asyncio.sleep(randint(2, 4))
                        #await self.simulation(link=link)
                        continue
                    else:
                        log("Não foi possivel Executar Ação de Curtida")
                        log(f"Vamos tentar o Like Novamente")
                        await self.click_like(user_name)
                        await asyncio.sleep(randint(2, 4))
                        if await self.curtido():
                            self.total_like += 1
                            log(f"{self.total_like} Ações Realizadas com Sucesso")
                            await asyncio.sleep(randint(2, 4))
                            #await self.simulation(link=link)
                            continue
                        else:
                            log("Não foi possivel Executar Ação de Curtida")
                            self.block_like += 1
                            await asyncio.sleep(randint(2, 4))
                            #await self.simulation(link=link)
                        if self.block_like >= 24:
                            with open("block.log", "a", encoding="utf-8") as blc:
                                blc.write(f"{self.profile} esta com Bloqueio de Curtir --> {datetime.now()}\n")
                            log(f"{self.profile} esta com Block like")
                            break           
                except Exception as erro:
                    log(f"Deu Ruim: {erro}")
                    log("Erro ao Abri o link do Tiktok")
                    await asyncio.sleep(randint(1, 3))
                    continue
            
            await self.tiktok.close()
            await asyncio.sleep(randint(2,4))
            await self.check_tasks()
            log(f"Total de {self.total_like} Ações Realizadas com Sucesso")
            log("Vamos Trocar para outro Perfil")
            await asyncio.sleep(randint(3,6))
            break
            # if self.total_like >= 50:
            #     log("Meta de Ações Concluida")
            #     log("Vamos mudar de Profile")
            #     return True
            
            # try:
            #     await self.get_like.reload()
            #     await asyncio.sleep(randint(3,6))
            #     if await self.logged_in_to_getlike():
            #         log("Verificando se tem +Ações...")
            #         await self.unlock_tasks()
            #         await asyncio.sleep(randint(1,2))
            #         list_links = await self.get_tasks()
            #         log(f"Temos mais {len(list_links)} Ações...")
            #         if len(list_links) == 0:
            #             log("No momento estamos sem Ações! Vamos Trocar para outro Perfil")
            #             break
            #     else:
            #         log("Vamos mudar de Profile")
            #         break
            # except Exception as erro:
            #     log(f"Erro: {erro}")



    async def run(self):
        while True:
            try:
                await self.like()
                await self.continuar()
            except Exception as erro:
                log(f"Erro: {erro}")
                await asyncio.sleep(30)
                
    
    async def constructor(self):
        try:
            await self.login_getlike()
            await self.set_tab_tiktok()
            await self.login_profile()
        except Exception as erro:
            log(f"Erro: {erro}")        
                
system = System()
