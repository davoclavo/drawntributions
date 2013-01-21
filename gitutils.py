from git import Repo, Commit, Actor
from cStringIO import StringIO
from gitdb import IStream

# TO DO
# =====
# Intialize git repo using GitPython
# Create a custom Committer and Author - using a name and an email

path = '/home/dav/dev/testgit/'
repo = Repo(path)
filename = path + "bulgogi"

def datecommit(date):
    try:
        data = repo.head.commit.hexsha
    except ValueError:
        data = 'First Commit, Baby'
    with open(filename, "w+") as file:
        # data = file.read()
        file.write(data)
        file.close()
    repo.index.add([filename])
    newcommit(repo, str(date), int(date.strftime('%s')))


def newcommit(repo, message, date, name=None, email=None):
    """Creates a commit object with a custom date.
    :param repo: Repo object the commit should be part of
    :param tree: Tree object
    :param message: Commit message. It may be an empty string
                    if no message is provided.
    :param date: Date in seconds, as an Int
    :return: Commit object representing the new commit
    :note:
        Additional information about the committer and Author are taken from
        the git configuration
    """

    tree = repo.index.write_tree()
    try:
        parents = [repo.head.commit]
    except ValueError:
        parents = []

    # Committer and Author info
    cr = repo.config_reader()
    if name == None or email == None:
        actor = Actor.committer(cr)
    else:
        actor = Actor(name, email)

    committer = actor
    author = actor

    # Date
    # offset = altzone # 3600*offsethours
    offset = 0  # UTC

    author_time, author_offset = date, offset
    committer_time, committer_offset = date, offset

    # assume utf8 encoding
    enc_section, enc_option = Commit.conf_encoding.split('.')
    conf_encoding = cr.get_value(enc_section,
                                 enc_option,
                                 Commit.default_encoding)

    # Create New Commit
    new_commit = Commit(repo, Commit.NULL_BIN_SHA, tree,
                    author, author_time, author_offset,
                    committer, committer_time, committer_offset,
                    message, parents, conf_encoding)

    stream = StringIO()
    new_commit._serialize(stream)
    streamlen = stream.tell()
    stream.seek(0)

    istream = repo.odb.store(IStream(Commit.type, streamlen, stream))
    new_commit.binsha = istream.binsha

    # Advance HEAD to the new commit automatically.
    # need late import here, importing git at the very beginning throws.
    import git.refs
    try:
        repo.head.set_commit(new_commit, logmsg="commit: %s" % message)
    except ValueError:
        # head is not yet set to the ref our HEAD points to
        # Happens on first commit
        import git.refs
        master = git.refs.Head.create(repo, repo.head.ref,
                                      new_commit, logmsg="commit (initial): %s" % message)
        repo.head.set_reference(master, logmsg='commit: Switching to %s' % master)
    # END handle empty repositories
    return new_commit
