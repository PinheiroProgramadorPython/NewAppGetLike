from nodriver import Browser, Config, Tab
from pathlib import Path
from shutil import rmtree, copy2, copytree
import os
from datetime import datetime
from app.logger import detectar_profile, log
import requests



class Navegador(Browser):
    def __init__(self, config: Config = None):
        self.profile = detectar_profile()
        self.api = "7966e8f8296fca63c52915368c60bc18"
        self.navegador_visivel = True
        self.nav = None
        self.new_nav = None
        self.page = None
        self.path_chrome = Path.cwd()/"chrome"/"nav_getlike.exe"
        self.profile_default = Path.cwd()/"perfil_chrome"/"profile_default"
        self.path_profile = Path.cwd()/"perfil_chrome"/self.profile
        self.path_profile_dolphin = Path.cwd()/"profiles_dolphin"/self.profile
        self.backup = Path.cwd()/"backup"/self.profile
        os.makedirs(self.backup, exist_ok=True)
        self.homepage = "https://getlike.io/en/tasks/tiktok/like/"
        self.extension = Path.cwd()/"buster"
        self.extension2 = Path.cwd()/"sad_captcha"
        self.extension3 = Path.cwd()/"CapSolver"
        self.host = "p.nxt.ge"
        self.port = 1769
        self.user = "valdir"
        self.senha = "799fbd33"
        self.proxy = "http://valdir:799fbd33@p.nxt.ge:1769"
        self.time_zone = "America/Sao_Paulo"
        self.config = Config(
            user_data_dir = self.path_profile,
            headless = False,
            browser_executable_path = self.path_chrome,
            lang = "pt-BR",
            sandbox= True,
            browser_args = [
                "--mute-audio",
                "--window-size=670,730",
                "--window-position=-0,0",
                "--disable-renderer-backgrounding",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-gpu",
                "--use-gl=swiftshader",           
                "--disable-software-rasterizer",
                "--ascii-canvas-render",
                "--no-zygote",
                "--disable-translate",
                "--hide-crash-restore-bubble",
                "--disable-features=WebRtcHideLocalIpsWithMdns,RendererCodeIntegrity,IsolateOrigins,site-per-process,CalculateNativeWinOcclusion,PrivacySandboxSettings4,Translate,TranslateUI",
                # "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"                             
            ]   
        )
        self.config.add_extension(self.extension)
        # self.config.add_extension(self.extension2)
        config = self.config
        super().__init__(config)
        
        
  
 
    async def iniciar(self):
        self.nav = await self.start()
        self.page = await self.get(self.homepage)
        return self.nav
    
    
    async def iniciar_dolphin(self):
        profile_id = "717896061"
        nav = requests.get(f"http://localhost:3001/v1.0/browser_profiles/{profile_id}/start?automation=1").json()
        self.nav = await self.create(browser_executable_path=None, browser_args=[f"--remote-debugging-port={nav}"])
        self.nav.get(self.homepage)
        #self.page = await self.get(self.homepage)
        return self.nav
    
    
    async def init(self):
        self.nav = await make_nodriver_solver(self.api, browser_executable_path = self.config.browser_executable_path, user_data_dir = self.config.user_data_dir, browser_args = self.config._default_browser_args)
        self.page = await self.nav.get(self.homepage)
        return await self.nav
    
        
    async def create_new_context(self):
        self.new_nav = await self.create_context(proxy_server=self.proxy)
        return self.new_nav
    
    
    async def show_browser(self):
        try:
            if self.navegador_visivel:
                await self.page.set_window_size(left=-2000, top=-2000, width=670, height=730)
                self.navegador_visivel = False                     
            else:
                await self.page.set_window_size(left=0, top=0, width=670, height=730)
                self.navegador_visivel = True
        except Exception as erro:
            log(f"Erro ao Manipular Navegador: {erro}")
            

    async def matar_chromium(self):
        try: 
            # os.system("taskkill /F /IM nav_getlike.exe >nul 2>&1")   
            return await os.system("taskkill /F /IM nav_getlike.exe /T") 
        except Exception as erro:
            return log("Navegador não Encontrado")
        
        
    def create_profile(self):
        copytree(self.profile_default, self.path_profile)
        log(f"Pasta: {self.path_profile} Criada com Sucess")
    

    def _backup(self):
        try:
            if self.path_profile:
                local_state = Path(self.path_profile/"Local State")
                local_storage = Path(self.path_profile/"Default"/"Local Storage")
                network = Path(self.path_profile/"Default"/"Network")
                try:    
                    copy2(local_state, self.backup)
                    log(f"Arquivo Local State Salvo com Sucesso")
                except Exception as erro:
                    log(f"Deu Ruim\nErro: {erro}")
                    
                try:
                    rmtree(self.backup/"Local Storage")
                except Exception as erro:
                    log(f"Deu Ruim\nErro: {erro}")
                finally:
                    copytree(local_storage, self.backup/"Local Storage")
                    log(f"Pasta Local Storage Salvo com Sucesso")
                
                try:
                    rmtree(self.backup/"Network")
                except Exception as erro:
                    log(f"Deu Ruim\nErro: {erro}")
                finally:
                    copytree(network, self.backup/"Network")
                    log(f"Pasta Network Salvo com Sucesso")
                    
                try:
                    rmtree(self.path_profile)
                    log(f"Pasta: {self.path_profile} foi Removida com Sucesso!")
                except Exception as erro:
                    log(f"Deu Ruim\nErro: {erro}")         
        except Exception as erro:
            log(f"Deu Ruim\nErro: {erro}")
            
            
    async def restore(self):
        try: 
            local_state = Path(self.backup/"Local State")
            local_storage = Path(self.backup/"Local Storage")
            network = Path(self.backup/"Network")
            default = Path(self.path_profile/"Default")
            
            self.create_profile()
            
            if self.path_profile:
                try:
                    copy2(local_state, self.path_profile)
                    log(f"Arquivo Local State Restaurado com Sucesso")
                except Exception as erro:
                    log(f"Deu Ruim\nErro: {erro}")
                    
                try:
                    rmtree(default/"Local Storage")
                except Exception as erro:
                    log(f"Deu Ruim\nErro: {erro}")
                finally:
                    copytree(local_storage, default/"Local Storage")
                    log(f"Pasta Local Storage Restaurado com Sucesso")
                    
                try:
                    rmtree(default/"Network")
                except Exception as erro:
                    log(f"Deu Ruim\nErro: {erro}")
                finally:
                    copytree(network, default/"Network")
                    log(f"Pasta Network Restaurado com Sucesso")
        except Exception as erro:
            log(f"Deu Ruim\nErro: {erro}")


    
            

# browser_args = [
#     "--autoplay-policy=no-user-gesture-required",   
#     "--disable-backgrounding-occluded-windows", 
#     "--disable-background-timer-throttling", 
#     "--disable-background-networking", 
#     "--disable-renderer-backgrounding",
#     "--disable-gesture-requirement-for-presentation",
#     "--disable-popup-blocking",
#     "--disable-ios-password-suggestions",
#     "--disable-login-screen-apps",
#     "--disable-notifications",
#     "--disable-oobe-network-screen-skipping-for-testing",
#     "--disable-origin-trial-controlled-blink-features",
#     "--disable-per-user-timezone",
#     "--disable-policy-key-verification",
#     "--disable-site-isolation-for-policy",
#     "--disable-third-party-keyboard-workaround",
#     "--disallow-policy-block-dev-mode",
#     "--mute-audio",
#     "--no-first-run",
#     "--window-size=700,700",   
# ]

# "--disable-features=Translate",      # 1. Desativa a barra de Tradução
# "--disable-infobars",                # 2. Remove barras de aviso e a barra de tradução
# "--disable-notifications",           # 3. Remove prompts de notificação de site
# "--no-default-browser-check",        # 4. Remove a verificação de navegador padrão
# "--noerrdialogs",



# <div class="TUXModal captcha-verify-container" data-width="small" aria-labelledby=":r0:_title" tabindex="0" id=":r1:" role="dialog" style="width: 380px; max-width: unset; z-index: 8000;"><div id="captcha-verify-container-main-page" aria-modal="true" role="main" class="cap-flex cap-py-4 cap-px-12 sm:cap-px-16 sm:cap-py-12 cap-flex-col cap-justify-between cap-h-full sm:cap-w-[380px]"><div class="cap-flex cap-flex-row-reverse sm:cap-flex-col cap-justify-end sm:cap-justify-start cap-gap-2 cap-w-full cap-mb-8"><div class="cap-flex cap-flex-row-reverse cap-items-center cap-flex-shrink-0   }"><button class="TUXButton TUXButton--borderless TUXButton--xsmall TUXButton--secondary" aria-disabled="false" type="button" id="captcha_close_button" role="button" aria-label="Fechar" aria-live="polite"><div class="TUXButton-content"><div class="TUXButton-iconContainer"><svg fill="currentColor" color="inherit" font-size="20" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"><path d="M10.19 36.19a1 1 0 0 1 0-1.42L20.96 24 10.19 13.23a1 1 0 0 1 0-1.42l1.62-1.62a1 1 0 0 1 1.42 0L24 20.96l10.77-10.77a1 1 0 0 1 1.42 0l.09.09.01.01 1.42 1.42.01.01.1.1a1 1 0 0 1 0 1.4L27.03 24l10.77 10.77a1 1 0 0 1 0 1.42l-.1.09v.01l-1.42 1.42-.1.1a1 1 0 0 1-1.42 0L24 27.04 13.23 37.81a1 1 0 0 1-1.42 0L10.2 36.2Z"></path></svg></div></div></button></div><div class="cap-flex cap-items-center cap-flex-1 cap-min-w-0 "><span class="cap-break-words cap-text-left" style="color: var(--ui-text-1); font-size: 16px; font-weight: inherit; font-family: var(--tux-web-font-body);">Arraste o controle deslizante para encaixar o quebra-cabeças</span></div></div><div class="cap-flex cap-flex-col cap-w-full cap-justify-center cap-min-h-[180px]"><div class="cap-flex cap-flex-col cap-justify-center cap-items-center "><img src="blob:https://www.tiktok.com/0a60f626-e720-4ea5-9711-8affd47804c8" alt="Captcha" class="cap-h-[170px] sm:cap-h-[210px]" draggable="false" style="clip-path: circle(50%); display: flex; transform: rotate(0deg);"><img src="blob:https://www.tiktok.com/7907d20e-55d2-469a-bcc1-3d5da6c995bd" alt="Captcha" class="cap-absolute cap-h-[105px] sm:cap-h-[128px]" draggable="false" style="clip-path: circle(50%); transform: rotate(0deg); display: flex;"></div><div class="cap-flex cap-w-full cap-mt-6 cap-mb-4"><div class="cap-flex  cap-w-full cap-h-40 cap-rounded-full cap-bg-UISheetGrouped3"><div draggable="true" class="cap-flex cap-absolute " style="cursor: grab; transform: translateX(0px);"><button class="TUXButton TUXButton--default TUXButton--medium TUXButton--secondary TUXButton--disabled secsdk-captcha-drag-icon sm:cap-w-auto cap-ml-0 cap-shadow-md" aria-disabled="true" type="button" id="captcha_slide_button" style="opacity: 1; cursor: grab; border-radius: 32px; width: 64px; min-width: 24px;"><div class="TUXButton-content"><div class="TUXButton-iconContainer"><svg fill="currentColor" class="flip-rtl " color="inherit" font-size="inherit" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"><path d="m44.12 21.88-15.3-15.3a1 1 0 0 0-1.4 0L24.6 9.4a1 1 0 0 0 .02 1.43L35.26 21H5a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h30.26L24.62 37.17a1 1 0 0 0-.02 1.43l2.81 2.81a1 1 0 0 0 1.42 0l15.3-15.29a3 3 0 0 0 0-4.24Z"></path></svg></div></div></button></div></div></div></div><div class="cap-flex cap-flex-row cap-justify-between cap-items-center cap-w-full"><div></div><div class="cap-flex cap-flex-row"><div class="cap-text-[8px] cap-text-UITextPlaceholder cap-flex cap-flex-row cap-justify-between cap-items-center">2025111709334670BE92D2D1B38A3543C3</div><button class="TUXButton TUXButton--borderless TUXButton--xsmall TUXButton--secondary cap-flex cap-items-center cap-mx-4" aria-disabled="false" type="button" id="captcha_refresh_button"><div class="TUXButton-content"><div class="TUXButton-iconContainer"><svg fill="currentColor" color="inherit" font-size="20" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"><path d="M56.62 21a25.5 25.5 0 1 0 3.8 22.32c.13-.4.54-.63.94-.53l1.44.4c.4.1.64.51.53.9a28.5 28.5 0 1 1-4.83-25.6V8.26c0-.41.34-.75.75-.75h1.5c.41 0 .75.34.75.75v13.5c0 1.24-1 2.25-2.25 2.25h-13.5a.75.75 0 0 1-.75-.75v-1.5c0-.41.34-.75.75-.75h10.87Z"></path></svg></div></div></button><button class="TUXButton TUXButton--borderless TUXButton--xsmall TUXButton--secondary cap-flex cap-items-center cap-mx-4" aria-disabled="false" type="button" id="captcha_feedback_button"><div class="TUXButton-content"><div class="TUXButton-iconContainer"><svg fill="currentColor" color="inherit" font-size="20" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"><path d="M24 7.5a16.5 16.5 0 1 0 0 33 16.5 16.5 0 0 0 0-33ZM4.5 24a19.5 19.5 0 1 1 39 0 19.5 19.5 0 0 1-39 0Zm18-9.5c0-.28.22-.5.5-.5h2c.28 0 .5.22.5.5v13a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-13ZM24 30c-.83 0-1.5.67-1.5 1.5v1a1.5 1.5 0 0 0 3 0v-1c0-.83-.67-1.5-1.5-1.5Z"></path></svg></div></div></button></div></div></div></div>