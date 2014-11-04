from fabric.api import lcd,local
import os

def prepare_deployment(branch_name):
    local('python manage.py test healthcat_project')
    #local('git add -p && git commit') # or local('hg add && hg commit')
    try:
        commit = local('git add -p && git commit')
        if commit.failed:
            print 'Nothing to commit, exiting...'
            sys.exit(0)
    except SystemExit, e:
        print 'commit returned non-zero', e
    #local('git checkout master && git merge ' + branch_name)

def deploy():
    with lcd('../../Team134/healthcat_project'):
        print os.getcwd()
        # With git...
        local('git pull')

        # With both
        local('python manage.py makemigrations')
        try:
            migrate = local('python manage.py migrate')
            if migrate.failed:
                print 'Nothing to commit, exiting...'
                sys.exit(0)
        except SystemExit, e:
            print 'migrate returned non-zero', e
        local('python manage.py test healthcat')
        local('python manage.py runserver')