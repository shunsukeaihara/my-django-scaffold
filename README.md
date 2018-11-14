# python, Django

pyenv、direnvはインストール済みとする。とりあえず3.6系の最新を利用

```
brew install pipenv
pyenv install 3.6.6
```

グローバルの環境変数に以下を設定する。(プロジェクトのディレクトリに.venvを作成するようにする)

.zshrcとかに以下を追加。

```
export PIPENV_VENV_IN_PROJECT=true
```

## pipenvの作成

```
pipenv install --python=3.6.6
```

## direnvでpathを設定

.envrcに.vnevへのパスを設定

```
export PATH="/path/to/projectdir/.venv/bin:$PATH"
```

# vue

```
npm install -g @vue/cli
cd js
npm install
```

## 作り方

vue-cli3で作る


# nuxt


## 作り方

```
npx create-nuxt-app
> Generating Nuxt.js project in /Users/aihara/work/django-template/template
? Project name template
? Project description My best Nuxt.js project
? Use a custom server framework express
? Use a custom UI framework vuetify
? Choose rendering mode Universal
? Use axios module no
? Use eslint yes
? Use prettier no
? Author name aihara
? Choose a package manager npm
```

axiosは自前でいろいろいじるのでモジュールは使わない. prettierもatomでやる(というかbeautifyを使っている)
