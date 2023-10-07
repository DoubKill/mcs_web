import os
import subprocess
import tarfile
import shutil


def package():
    print("start package mcs_web")
    # 删除旧打包文件
    if os.path.exists("dist"):
        shutil.rmtree('dist')
        print("remove dist dir successfully")
    if os.path.exists("build"):
        shutil.rmtree('build')
        print("remove build dir successfully")
    if os.path.exists("mcs_web_linux.tar.gz"):
        os.system('rm -rf mcs_web_linux.tar.gz')
        print("remove mcs_web_linux.tar.gz dir successfully")
    # 删除旧前端文件
    if os.path.exists("fronted"):
        shutil.rmtree('fronted')
        print("remove fronted dir successfully")
    # 拷贝最新前端文件并重命名
    shutil.copytree('../mcsfront/dist', 'fronted')

    # 打包run_wsgi
    os.system("pyinstaller run_wsgi.spec --noconfirm")
    # 备份run_asgi
    print('copy run_wsgi to dist')
    shutil.copyfile('dist/mcs_web/run_wsgi', 'dist/run_wsgi')
    # 打包manage
    os.system("pyinstaller manage.spec --noconfirm")

    # 拷贝迁移文件
    shutil.copytree('agv/migrations/', 'dist/mcs_web/agv/migrations')
    shutil.copytree('basics/migrations/', 'dist/mcs_web/basics/migrations')
    shutil.copytree('monitor/migrations/', 'dist/mcs_web/monitor/migrations')
    shutil.copytree('openapi/migrations/', 'dist/mcs_web/openapi/migrations')
    shutil.copytree('user/migrations/', 'dist/mcs_web/user/migrations')
    os.chdir("dist/mcs_web")

    # 移动run_asgi
    shutil.move('../run_wsgi', '.')
    # 赋权
    subprocess.run(["chmod", "+x", "run_wsgi"])
    subprocess.run(["chmod", "+x", "manage"])
    subprocess.run(["chmod", "+x", "run.sh"])
    # 生成打包压缩文件
    print("tar file")
    os.chdir("../..")
    try:
        with open('../version', 'r', encoding='utf-8') as f:
            version = f.read()
    except Exception as e:
        version = ''
    tar_filename = "mcs_web_linux_{}.tar.gz".format(version)
    source_dir = "dist/mcs_web"
    with tarfile.open(tar_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    print("tar file successfully")
    print("package mcs_web successfully")


if __name__ == '__main__':
    package()
