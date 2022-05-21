WHOAMI_QUERY = '''
query {
    whoami {
        username
        profileColor
        isSuperuser
        profilePictureFilename
        email
        notes {
            id
        }
    }
}
'''
