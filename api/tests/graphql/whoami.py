WHOAMI_QUERY = '''
query {
    whoami {
        user {
            username
            profileColor
            isSuperuser
            profilePictureFilename
        }
        email
    }
}
'''
