from webkitpy.common.system.filesystem import FileSystem
from webkitpy.common.system.filesystem_mock import MockFileSystem
from webkitpy.common.checkout.scm.detection import detect_scm_system
from webkitpy.common.checkout.scm.git import Git, AmbiguousCommitError
from webkitpy.common.checkout.scm.scm import SCM
from webkitpy.common.checkout.scm.svn import SVN
import webkitpy.thirdparty.unittest2 as unittest
original_cwd = None
def delete_cached_svn_repo_at_exit():
        os.chdir(original_cwd)
        shutil.rmtree(cached_svn_repo_path)
class SCMTestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SCMTestBase, self).__init__(*args, **kwargs)
        self.scm = None
        self.executive = None
        self.fs = None
        self.original_cwd = None
    def setUp(self):
        self.executive = Executive()
        self.fs = FileSystem()
        self.original_cwd = self.fs.getcwd()
    def tearDown(self):
        self._chdir(self.original_cwd)
    def _join(self, *comps):
        return self.fs.join(*comps)
    def _chdir(self, path):
        self.fs.chdir(path)
    def _mkdir(self, path):
        assert not self.fs.exists(path)
        self.fs.maybe_make_directory(path)
    def _mkdtemp(self, **kwargs):
        return str(self.fs.mkdtemp(**kwargs))
    def _remove(self, path):
        self.fs.remove(path)
    def _rmtree(self, path):
        self.fs.rmtree(path)
    def _run(self, *args, **kwargs):
        return self.executive.run_command(*args, **kwargs)
    def _run_silent(self, args, **kwargs):
        self.executive.run_and_throw_if_fail(args, quiet=True, **kwargs)
    def _write_text_file(self, path, contents):
        self.fs.write_text_file(path, contents)
    def _write_binary_file(self, path, contents):
        self.fs.write_binary_file(path, contents)
    def _make_diff(self, command, *args):
        # We use this wrapper to disable output decoding. diffs should be treated as
        # binary files since they may include text files of multiple differnet encodings.
        return self._run([command, "diff"] + list(args), decode_output=False)
    def _svn_diff(self, *args):
        return self._make_diff("svn", *args)
    def _git_diff(self, *args):
        return self._make_diff("git", *args)
    def _svn_add(self, path):
        self._run(["svn", "add", path])
    def _svn_commit(self, message):
        self._run(["svn", "commit", "--quiet", "--message", message])
    def _set_up_svn_checkout(self):
        global original_cwd
            cached_svn_repo_path = self._set_up_svn_repo()
            original_cwd = self.original_cwd

        self.temp_directory = self._mkdtemp(suffix="svn_test")
        self.svn_repo_path = self._join(self.temp_directory, "repo")
        self.svn_repo_url = "file://%s" % self.svn_repo_path
        self.svn_checkout_path = self._join(self.temp_directory, "checkout")
        shutil.copytree(cached_svn_repo_path, self.svn_repo_path)
        self._run(['svn', 'checkout', '--quiet', self.svn_repo_url + "/trunk", self.svn_checkout_path])

    def _set_up_svn_repo(self):
        svn_repo_path = self._mkdtemp(suffix="svn_test_repo")
        self._run(['svnadmin', 'create', '--pre-1.5-compatible', svn_repo_path])
        svn_checkout_path = self._mkdtemp(suffix="svn_test_checkout")
        self._run(['svn', 'checkout', '--quiet', svn_repo_url, svn_checkout_path])
        self._chdir(svn_checkout_path)
        self._mkdir('trunk')
        self._svn_add('trunk')
        self._svn_commit('add trunk')
        self._rmtree(svn_checkout_path)
        self._set_up_svn_test_commits(svn_repo_url + "/trunk")
    def _set_up_svn_test_commits(self, svn_repo_url):
        svn_checkout_path = self._mkdtemp(suffix="svn_test_checkout")
        self._run(['svn', 'checkout', '--quiet', svn_repo_url, svn_checkout_path])
        # Add some test commits
        self._chdir(svn_checkout_path)
        self._write_text_file("test_file", "test1")
        self._svn_add("test_file")
        self._svn_commit("initial commit")
        self._write_text_file("test_file", "test1test2")
        # This used to be the last commit, but doing so broke
        # GitTest.test_apply_git_patch which use the inverse diff of the last commit.
        # svn-apply fails to remove directories in Git, see:
        # https://bugs.webkit.org/show_bug.cgi?id=34871
        self._mkdir("test_dir")
        # Slash should always be the right path separator since we use cygwin on Windows.
        test_file3_path = "test_dir/test_file3"
        self._write_text_file(test_file3_path, "third file")
        self._svn_add("test_dir")
        self._svn_commit("second commit")
        self._write_text_file("test_file", "test1test2test3\n")
        self._write_text_file("test_file2", "second file")
        self._svn_add("test_file2")
        self._svn_commit("third commit")

        # This 4th commit is used to make sure that our patch file handling
        # code correctly treats patches as binary and does not attempt to
        # decode them assuming they're utf-8.
        self._write_binary_file("test_file", u"latin1 test: \u00A0\n".encode("latin-1"))
        self._write_binary_file("test_file2", u"utf-8 test: \u00A0\n".encode("utf-8"))
        self._svn_commit("fourth commit")

        # svn does not seem to update after commit as I would expect.
        self._run(['svn', 'update'])
        self._rmtree(svn_checkout_path)

    def _tear_down_svn_checkout(self):
        self._rmtree(self.temp_directory)
        self._mkdir("added_dir")
        self._write_text_file("added_dir/added_file", "new stuff")
        self.assertIn("added_dir/added_file", self.scm._added_files())
        self._mkdir("added_dir")
        self._write_text_file("added_dir/added_file", "new stuff")
        self.assertIn("added_dir/added_file", self.scm._added_files())
        self.assertNotIn("added_dir", self.scm._added_files())
        self._mkdir("added_dir")
        self._write_text_file("added_dir/added_file", "new stuff")
        self._write_text_file("added_dir/another_added_file", "more new stuff")
        self.assertIn("added_dir/added_file", self.scm._added_files())
        self.assertIn("added_dir/another_added_file", self.scm._added_files())
        self.assertIn("added_dir/another_added_file", self.scm._added_files())
        self._chdir(scm.checkout_root)
        self._write_text_file('foo.txt', 'some stuff')
        self._write_text_file('added_file', 'new stuff')
        self.assertIn('moved_file', self.scm._added_files())
        self._mkdir("added_dir")
        self._write_text_file('added_dir/added_file', 'new stuff')
        self._write_text_file('added_dir/another_added_file', 'more new stuff')
        self.assertIn('moved_dir/added_file', self.scm._added_files())
        self.assertIn('moved_dir/another_added_file', self.scm._added_files())

class SVNTest(SCMTestBase):
        super(SVNTest, self).setUp()
        self._set_up_svn_checkout()
        self._chdir(self.svn_checkout_path)
        super(SVNTest, self).tearDown()
        self._tear_down_svn_checkout()
        self._chdir(self.svn_checkout_path)
        self.assertIn("test_file", self.scm._deleted_files())
        self._chdir(self.svn_checkout_path)
        self.assertIn("test_file", self.scm._deleted_files())
        self.assertIn("test_file2", self.scm._deleted_files())
class GitTest(SCMTestBase):
    def setUp(self):
        super(GitTest, self).setUp()
        self._set_up_git_checkouts()
    def tearDown(self):
        super(GitTest, self).tearDown()
        self._tear_down_git_checkouts()
    def _set_up_git_checkouts(self):
        """Sets up fresh git repository with one commit. Then sets up a second git repo that tracks the first one."""

        self.untracking_checkout_path = self._mkdtemp(suffix="git_test_checkout2")
        self._run(['git', 'init', self.untracking_checkout_path])

        self._chdir(self.untracking_checkout_path)
        self._write_text_file('foo_file', 'foo')
        self._run(['git', 'add', 'foo_file'])
        self._run(['git', 'commit', '-am', 'dummy commit'])
        self.tracking_git_checkout_path = self._mkdtemp(suffix="git_test_checkout")
        self._run(['git', 'clone', '--quiet', self.untracking_checkout_path, self.tracking_git_checkout_path])
        self._chdir(self.tracking_git_checkout_path)
    def _tear_down_git_checkouts(self):
        self._run(['rm', '-rf', self.tracking_git_checkout_path])
        self._run(['rm', '-rf', self.untracking_checkout_path])
        self.assertEqual(self.tracking_scm._remote_branch_ref(), 'refs/remotes/origin/master')
        self._chdir(self.untracking_checkout_path)
        self.assertRaises(ScriptError, self.untracking_scm._remote_branch_ref)
        self._run(['git', 'config', '--add', 'svn-remote.svn.fetch', 'trunk:remote1'])
        self._run(['git', 'config', '--add', 'svn-remote.svn.fetch', 'trunk:remote2'])
        self.assertEqual(self.tracking_scm._remote_branch_ref(), 'remote1')
        self._write_text_file('test_file_commit1', 'contents')
        self._run(['git', 'add', 'test_file_commit1'])
class GitSVNTest(SCMTestBase):
        super(GitSVNTest, self).setUp()
        self._set_up_svn_checkout()
        self._set_up_gitsvn_checkout()
        super(GitSVNTest, self).tearDown()
        self._tear_down_svn_checkout()
        self._tear_down_gitsvn_checkout()

    def _set_up_gitsvn_checkout(self):
        self.git_checkout_path = self._mkdtemp(suffix="git_test_checkout")
        # --quiet doesn't make git svn silent
        self._run_silent(['git', 'svn', 'clone', '-T', 'trunk', self.svn_repo_url, self.git_checkout_path])
        self._chdir(self.git_checkout_path)

    def _tear_down_gitsvn_checkout(self):
        self._rmtree(self.git_checkout_path)
        self._run(['git', 'config', key, value])
        test_file = self._join(self.git_checkout_path, 'test_file')
        self._write_text_file(test_file, 'foo')
        self._run(['git', 'commit', '-a', '-m', 'local commit'])
        self.assertEqual(len(self.scm._local_commits()), 1)
        test_file = self._join(self.git_checkout_path, 'test_file')
        self._write_text_file(test_file, 'foo')
        self._run(['git', 'commit', '-a', '-m', 'local commit'])
        self.assertEqual(len(self.scm._local_commits()), 1)
        self.scm._discard_local_commits()
        self.assertEqual(len(self.scm._local_commits()), 0)
        self._run(['git', 'checkout', '-b', new_branch])
        self.assertEqual(self._run(['git', 'symbolic-ref', 'HEAD']).strip(), 'refs/heads/' + new_branch)
        self._run(['git', 'checkout', '-b', 'bar'])
        self.assertNotRegexpMatches(self._run(['git', 'branch']), r'foo')
        svn_test_file = self._join(self.svn_checkout_path, 'test_file')
        self._write_text_file(svn_test_file, "svn_checkout")
        self._run(['svn', 'commit', '--message', 'commit to conflict with git commit'], cwd=self.svn_checkout_path)
        git_test_file = self._join(self.git_checkout_path, 'test_file')
        self._write_text_file(git_test_file, "git_checkout")
        self._run(['git', 'commit', '-a', '-m', 'commit to be thrown away by rebase abort'])
        # Should fail due to a conflict leaving us mid-rebase.
        # we use self._run_slient because --quiet doesn't actually make git svn silent.
        self.assertRaises(ScriptError, self._run_silent, ['git', 'svn', '--quiet', 'rebase'])
        self.assertTrue(self.scm._rebase_in_progress())
        self.scm._discard_working_directory_changes()
        self.assertFalse(self.scm._rebase_in_progress())
        self.scm._discard_working_directory_changes()
        self._write_text_file(filename, contents)
        self._run(['git', 'add', filename])
        self._write_text_file('test_file_commit2', 'still more test content')
        self._run(['git', 'add', 'test_file_commit2'])
        self._write_text_file('test_file', 'changed test content')
        self._write_text_file('test_file', 'changed test content')
    def _test_upstream_branch(self):
        self._run(['git', 'checkout', '-t', '-b', 'my-branch'])
        self._run(['git', 'checkout', '-t', '-b', 'my-second-branch'])
        self.assertEqual(self.scm._remote_branch_ref(), 'refs/remotes/trunk')
        self._run(['git', 'checkout', '-b', 'dummy-branch', 'trunk~3'])
        self._run(['git', 'merge', 'trunk'])
        self._remove('test_file_commit1')
        self._run(['git', 'checkout', '-b', 'my-branch', 'trunk~3'])
        test_file_path = self.fs.join(self.git_checkout_path, test_file_name)
        self._write_binary_file(test_file_path, file_contents)
        self._run(['git', 'add', test_file_name])
        self._write_binary_file(test_file_path, file_contents)
        self._run(['git', 'add', test_file_name])
        self._run(['git', 'commit', '-m', 'binary diff'])

        self._run(['git', 'checkout', '-b', 'my-branch', 'trunk~3'])
        self._run(['git', 'checkout', '-t', '-b', 'my-branch'])
        self._run(['git', 'checkout', '-t', '-b', 'my-second-branch'])
        self._write_text_file('test_file_commit0', 'more test content')
        self._run(['git', 'add', 'test_file_commit0'])
        self.assertIn("test_file_commit1", self.scm._deleted_files())
        self.assertIn("test_file_commit1", self.scm._deleted_files())
        self.assertIn("test_file_commit2", self.scm._deleted_files())
class GitTestWithMock(SCMTestBase):
    def make_scm(self):