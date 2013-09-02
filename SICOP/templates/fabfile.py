# -*- coding: utf-8 -*-
import os
import tempfile
from sgf.settings import DATABASES, TABELAS_AUDITADAS

FABRIC_ROOT = os.path.dirname(os.path.abspath(__file__))

from fabric.api import *

PID_VALIDACAO = os.path.join(tempfile.gettempdir(), 'sigef_celery_validacao.pid')
PID_PERSISTENCIA = os.path.join(tempfile.gettempdir(), 'sigef_celery_persistencia.pid')


def worker_persistencia():
    local('./manage.py celery worker -E -c 1 -n persistencia -Q persistencia -l info --pidfile=%s &' % PID_PERSISTENCIA)


def kill_worker_persistencia():
    local('kill `cat %s`' % PID_PERSISTENCIA)


def worker_validacao():
    local('./manage.py celery worker -E -n validacao -Q validacao -l info --pidfile=%s &' % PID_VALIDACAO)


def kill_worker_validacao():
    local('kill `cat %s`' % PID_VALIDACAO)


def _executar_arquivo_psql(host, porta, banco, user, arquivo):
    """
    Executa um arquivo psql no banco
    """

    local("psql -h %(host)s -P %(porta)s -U %(usuario)s -d %(banco)s -f \"%(arquivo)s\"" % {"host": host,
                                                                                            "porta": porta,
                                                                                            "banco": banco,
                                                                                            "arquivo": arquivo,
                                                                                            "usuario": user})


def _executar_comando_psql(host, porta, banco, user, comando):
    """
    Executa um comando psql no banco
    """

    local("psql -h %(host)s -P %(porta)s -U %(usuario)s -d %(banco)s -c \"%(comando)s\"" % {"host": host,
                                                                                            "porta": porta,
                                                                                            "banco": banco,
                                                                                            "comando": comando,
                                                                                            "usuario": user})


def instalar_audit_log():
    """
    Instala os logs de audit
    no postgresql
    """

    if not "default" in DATABASES:
        local("echo Não foi possível importar o database default.")

    dd = DATABASES["default"]
    usuario = dd["USER"]
    host = dd["HOST"]
    porrrrrta = dd["PORT"]
    banco = dd["NAME"]
    audit_sql = os.path.join(FABRIC_ROOT, "..", "deploy", "audit.sql")

    _executar_arquivo_psql(host, porrrrrta, banco, usuario, audit_sql)


def auditar_tudo():
    if not "default" in DATABASES:
        local("echo Não foi possível importar o database default.")

    tabelas = TABELAS_AUDITADAS
    for tabela in tabelas:
        auditar_tabela(tabela)


def auditar_tabela(tabela):
    if not "default" in DATABASES:
        local("echo Não foi possível importar o database default.")

    dd = DATABASES["default"]
    usuario = dd["USER"]
    host = dd["HOST"]
    porrrrrta = dd["PORT"]
    banco = dd["NAME"]

    comando = "SELECT audit.audit_table('%s');" % tabela

    _executar_comando_psql(host, porrrrrta, banco, usuario, comando)


def workers():
    worker_validacao()
    worker_persistencia()


def kill_workers():
    kill_worker_validacao()
    kill_worker_persistencia()
