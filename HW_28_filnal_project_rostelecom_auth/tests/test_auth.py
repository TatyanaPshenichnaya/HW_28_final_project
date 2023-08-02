import pytest
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = 'https://b2c.passport.rt.ru'
valid_email = 'yarren.tester@gmail.com'
valid_password = 'Ab123456&'

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # ставим величину неявного ожидания элементов в 10 секунд
    # Переходим на страницу авторизации
    driver.get(base_url)

    yield driver

    driver.quit()

@pytest.fixture(autouse=True)
def driver_():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # ставим величину неявного ожидания элементов в 10 секунд
    # Переходим на страницу авторизации
    driver.get(base_url)

    yield driver

    driver.quit()


def test_auth_form_elements_tabs(driver):
   # Проверим наличие элементов на странице (таб авторизации)
   assert ( driver.find_element(By.ID, 't-btn-tab-phone').text == "Телефон" and
            driver.find_element(By.ID, 't-btn-tab-mail').text == "Почта"  and
            driver.find_element(By.ID, 't-btn-tab-login').text == "Логин" and
            driver.find_element(By.ID, 't-btn-tab-ls').text == "Лицевой счёт")


def test_auth_form_changing_tabs_email(driver):
    # Проверим смену табов при вводе данных определенного формата
    driver.find_element(By.ID, 't-btn-tab-phone').click()
    driver.find_element(By.ID, 'username').send_keys('mail@mail.ru')
    driver.find_element(By.ID, 'kc-login').click()  # нажимаем на кнопку "войти"
    #print(driver.find_element(By.XPATH, '//div/input[@name="tab_type"]/@value'))

    assert driver.find_element(By.CLASS_NAME, 'rt-tab--active').text == 'Почта'

def test_auth_form_changing_tabs_phone(driver):
    # Проверим смену табов при вводе данных определенного формата
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys('+7 910 666-49-08')
    driver.find_element(By.ID, 'kc-login').click()  # нажимаем на кнопку "войти"
    assert driver.find_element(By.CLASS_NAME, 'rt-tab--active').text == 'Телефон'

def test_auth_form_lc_mistake(driver):
    # Проверим появление сообщения об ошибке при вводе неверного формата лицевого счета
    driver.find_element(By.ID, 't-btn-tab-ls').click()
    driver.find_element(By.ID, 'username').send_keys('+7 910 666-49-08')
    driver.find_element(By.ID, 'kc-login').click()  # нажимаем на кнопку "войти"
    assert driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error').text == 'Проверьте, пожалуйста, номер лицевого счета'

def test_auth_form_changing_tabs_login(driver):
    # Проверим смену табов при вводе данных определенного формата
    driver.find_element(By.ID, 't-btn-tab-login').click()
    driver.find_element(By.ID, 'username').send_keys('+7 910 666-49-08')
    driver.find_element(By.ID, 'kc-login').click()  # нажимаем на кнопку "войти"
    assert driver.find_element(By.CLASS_NAME, 'rt-tab--active').text == 'Телефон'


@pytest.mark.parametrize("password", [valid_password, 'Ab654321'], ids=['Auth with valid password', 'Auth with invalid password'])
def test_auth_with_email(driver, password):
    # Проверим авторизацию с валидным и невалидным паролями
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(valid_email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'kc-login').click()  # нажимаем на кнопку "войти"

    # assert driver.find_element(By.CLASS_NAME, 'card-container__title').text == 'Авторизация'
    assert driver.find_element(By.CLASS_NAME, 'card-title').text == 'Учетные данные'


def test_password_recovering_elements(driver):
    # Проверка наличия элементов в форме восстановления пароля
    driver.find_element(By.ID, 'forgot_password').click()
    assert (driver.find_element(By.ID, 't-btn-tab-phone').text == "Телефон" and
            driver.find_element(By.ID, 't-btn-tab-mail').text == "Почта" and
            driver.find_element(By.ID, 't-btn-tab-login').text == "Логин" and
            driver.find_element(By.ID, 't-btn-tab-ls').text == "Лицевой счёт" and
            driver.find_element(By.ID, 'username') and
            driver.find_element(By.ID, 'captcha') and
            driver.find_element(By.ID, 'reset-back'))


def test_password_recovering_wrong_kapcha(driver):
    # Проверка восстановления пароля с помощью почты при неверном вводе в поле "капча"
    driver.find_element(By.ID, 'forgot_password').click()
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(valid_email)
    driver.find_element(By.ID, 'captcha').send_keys('aaaaaa')
    driver.find_element(By.ID, 'reset').click()
    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или текст с картинки'


def test_registration_elements(driver):
    # Проверка наличия элементов инетерфейса регистрации
    driver.find_element(By.ID, 'kc-register').click()
    assert (driver.find_element(By.NAME, 'firstName') and
            driver.find_element(By.NAME, 'lastName') and
            driver.find_element(By.ID, 'address') and
            driver.find_element(By.ID, 'password') and
            driver.find_element(By.ID, 'password-confirm')
            )


def test_registration_elements_negative(driver):
    # Проверка наличия элементов инетерфейса регистрации - кнопка "Продолжить"
    driver.find_element(By.ID, 'kc-register').click()
    assert driver.find_element(By.NAME, 'register').text == "Продолжить"

def test_registration_elements_link(driver):
    # Проверка наличия ссылки на политику конфиденциальности
    driver.find_element(By.ID, 'kc-register').click()
    assert driver.find_element(By.XPATH, '//a[@class="rt-link rt-link--orange"][starts-with(@href,"https://b2c.passport.rt.ru/sso-static/agreement/agreement")]')

def test_registration_nessesary_fill(driver):
    # Проверка обязательности заполнения полей инетерфейса регистрации
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'register').click()
    assert driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error').text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'



@pytest.mark.parametrize("name_input", ['д-', 'яФу', 'Катя', 'рябина-уу-', 'Ромашка2-2'])
def test_registration_name_checking_positive(driver, name_input):
    # Проверка на корректность заполнения поля для ввода имени и фамилии в интерфейсе регистрации
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(name_input)
    driver.find_element(By.NAME, 'lastName').send_keys(name_input)
    driver.find_element(By.NAME, 'register').click()
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.XPATH,
                            '//div[@class="name-container"]/div[@class="rt-input-container rt-input-container--error"]/span[@class="rt-input-container__meta rt-input-container__meta--error"][1]')


@pytest.mark.parametrize("name_input", ['Л', '', 'f', 'Yo', 'Ж5', 'ыRч', 'hello555ly',
                                      'СистемапроверяетнакорректностьвведенныеданныеполевводадолжносодержатьминимумсимволасостоящихизбуквкириллицыилизнакатиремапроверяетнакорректностьвведенныеданныеполевводадолжноСодержатьминимумсимволасостоящихизбуквкириллицыилизнакатирезнакатирезнакатирежжжж',
                                       'kjdgirotioHIUGHYIGkmnjkkrthJHiurgjknbfkcnowpouruiotyrgskldvjklsfjvbhshlkfhweuiotyeibjkfhvbjkdahfogiehriogweouopgupgjlsiiowquiyeovbzmiuoiurgsdjvlkjjjjjjjjioewyoeuiofpdvjpcjbklvhblhruiiwyoghvbdhjkhurytohgkjcbzdjbviwbilkfjghiwrjhgiuwrgvbkjbnkjrwhgfbdfwerrgge']
                         )
def test_registration_name_checking_negative(driver, name_input):
    # Проверка на корректность заполнения поля для ввода имени и фамилии в интерфейсе регистрации
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(name_input)
    driver.find_element(By.NAME, 'lastName').send_keys(name_input)
    driver.find_element(By.NAME, 'register').click()

    assert driver.find_element(By.XPATH, '//div[@class="name-container"]/div[@class="rt-input-container rt-input-container--error"]/span[@class="rt-input-container__meta rt-input-container__meta--error"][1]')

def test_registration_sending_validation_code(driver):
    # После заполнения формы регистрации валидными данными и нажатия на кнопку "Зарегистрироваться" система отправляет код подтверждения на email или телефон
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys('Катя')
    driver.find_element(By.NAME, 'lastName').send_keys('Лаптина')
    driver.find_element(By.ID, 'address').send_keys('gioufiug@gmail.com')
    driver.find_element(By.ID, 'password').send_keys(valid_password)
    driver.find_element(By.ID, 'password-confirm').send_keys(valid_password)
    driver.find_element(By.NAME, 'register').click()
    assert (driver.find_element(By.XPATH, '//h1[contains(text(), "Подтверждение email")]') and
            driver.find_element(By.ID, 'rt-code-0') and
            driver.find_element(By.ID, 'rt-code-1') and
            driver.find_element(By.ID, 'rt-code-2'))


def test_registration_unique_email_checking(driver):
    # Проверка уникальности введенного email при заполнения формы регистрации
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys('Катя')
    driver.find_element(By.NAME, 'lastName').send_keys('Лаптина')
    driver.find_element(By.ID, 'address').send_keys(valid_email)
    driver.find_element(By.ID, 'password').send_keys(valid_password)
    driver.find_element(By.ID, 'password-confirm').send_keys(valid_password)
    driver.find_element(By.NAME, 'register').click()
    assert driver.find_element(By.XPATH, '//h2[contains(text(), "Учётная запись уже существует")]')