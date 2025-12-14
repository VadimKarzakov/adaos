# Проверка сценария «Утренний сценарий» из консоли

Ниже — минимальные шаги, чтобы запустить локально сценарий `morning_routine` и увидеть его вывод в консоли без дополнительной инфраструктуры.

## 0. Где взять `api_key` для погоды
1. Создайте аккаунт на [openweathermap.org](https://openweathermap.org/) (подойдёт бесплатный тариф).
2. Зайдите в профиль → вкладка **API keys** и скопируйте ключ (обычно он отображается как «Default»). Если ключ только что создан, ему может потребоваться 10–15 минут, чтобы активироваться.
3. Этот ключ нужно подставить вместо заглушки `ВАШ_API_КЛЮЧ_OWM` в командах ниже.

## 1. Быстрый запуск одной командой (Linux/macOS, Bash)
Скопируйте и вставьте блок ниже в терминал из корня репозитория AdaOS. Он создаст виртуальное окружение, установит зависимости, сохранит API‑ключ для `weather_skill`, установит город «Москва» как последний использованный и запустит сценарий:

```bash
python -m venv .venv && \
source .venv/bin/activate && \
pip install -e . && \
ADAOS_BASE_DIR="$(pwd)/.adaos" PYTHONPATH="$(pwd)/src" \
python -m adaos.apps.cli.app skill run weather_skill setup --json '{"api_key":"ВАШ_API_КЛЮЧ_OWM"}' && \
ADAOS_BASE_DIR="$(pwd)/.adaos" PYTHONPATH="$(pwd)/src" \
python -m adaos.apps.cli.app skill run weather_skill get_weather --json '{"city":"Москва"}' && \
ADAOS_BASE_DIR="$(pwd)/.adaos" PYTHONPATH="$(pwd)/src" \
python -m adaos.apps.cli.app scenario run morning_routine --path .adaos/scenarios/scenarios
```

> Команда требует действующий ключ OpenWeatherMap (или совместимого API) — укажите его вместо `ВАШ_API_КЛЮЧ_OWM`. Запрос к погодному API выполняется один раз, чтобы сохранить город и убедиться, что ключ рабочий.

## 1а. Быстрый запуск в Windows PowerShell
Из каталога репозитория выполните команды ниже (каждая следующая команда зависит от успешного выполнения предыдущей):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
$env:ADAOS_BASE_DIR = "$PWD/.adaos"
$env:PYTHONPATH = "$PWD/src"
python -m adaos.apps.cli.app skill run weather_skill setup --json '{"api_key":"ВАШ_API_КЛЮЧ_OWM"}'
python -m adaos.apps.cli.app skill run weather_skill get_weather --json '{"city":"Москва"}'
python -m adaos.apps.cli.app scenario run morning_routine --path .adaos/scenarios/scenarios
```

Если при активации виртуального окружения PowerShell ругается на политику исполнения, запустите консоль от имени администратора и временно разрешите запуск локальных сценариев командой `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

## 2. Что вы увидите
- В консоли появится итоговое сообщение сценария, собранное из приветствия, времени и погоды.
- В конце команда выведет JSON c подробностями выполнения шагов и путём до лога (если он создан).

Если нужно переиспользовать этот сценарий в другом каталоге, скопируйте папку `.adaos` или укажите переменную `ADAOS_BASE_DIR` на другую директорию с установленными навыками и сценариями.
