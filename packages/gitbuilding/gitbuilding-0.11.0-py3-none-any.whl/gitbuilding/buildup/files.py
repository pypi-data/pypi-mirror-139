'''
This submodule contains the read directory function, a helper function so that the
contents of a whole directory can be passed into the Documentation object. It also
contains the FileInfo object. This is used to specify information about files that
are input into and output from BuildUp.

Note: No other buildup module should use os. And expecially not os.path
It causes confusion as it modifies paths into native paths, whereas buildup
is creating static markdown for html. It expects all internal paths to be
posix paths.

'''

#See note above about paths. Use posixpath for unless directly dealing with native files
import os
import posixpath
import logging
import regex as re
from gitbuilding.buildup.utilities import as_posix

_LOGGER = logging.getLogger('BuildUp')

def _pop_starting_with(pathlist, beginning):
    poplist = []
    for n, path in enumerate(pathlist):
        if path.startswith(beginning):
            poplist.append(n)
    #Pop them from the directory list in reverse order to keep indexes valid
    for n in poplist[::-1]:
        pathlist.pop(n)

def read_directory(path='.',
                   include_list=None,
                   exclude_list=None,
                   allow_hidden=False,
                   allow_leading_underscore=False):

    '''
    Recursively walks a directory and returns a list of all files as
    FileInfo objects. These objects contain only the path for all files
    except buildup files where they contain the contents of the file.
    '''

    if include_list is None:
        include_list = []
    if exclude_list is None:
        exclude_list = []

    # Use os.path/os.walk here we are dealing with files on local machine
    directory_files = []
    for filepath in include_list:
        directory_files.append(FileInfo(filepath))

    for root, dirs, files in os.walk(path):
        #find any hidden unix directories/files (inc .git) and
        #any beginning with an underscore

        if not allow_hidden:
            _pop_starting_with(dirs, '.')
            _pop_starting_with(files, '.')
        if not allow_leading_underscore:
            _pop_starting_with(dirs, '_')
            _pop_starting_with(files, '_')

        for file in files:
            if not os.path.basename(file) in exclude_list:
                page_path = os.path.join(root, file)
                page_path_rel = os.path.relpath(page_path, start=path)
                _warn_unsafe(page_path_rel)
                if file.endswith((".md", '.yml', '.yaml')):
                    with open(page_path, 'r', encoding='utf-8') as stream:
                        directory_files.append(FileInfo(page_path_rel,
                                                        dynamic_content=True,
                                                        content=stream.read()))
                else:
                    directory_files.append(FileInfo(page_path_rel))
    return directory_files

def _unsafe_chars(path):
    unsafe = re.findall(r'[^a-zA-z0-9\.\\\/\-_~ ]', path)
    if len(unsafe) > 0:
        chars = ''.join(set(unsafe))
    else:
        chars = ''
    return chars

def is_filepath_safe(path, allow_external=False):
    """
    Returns whether the file path is consider safe
    """
    if not allow_external:
        if as_posix(path).startswith('..'):
            return False
    return len(_unsafe_chars(path)) == 0

def _warn_unsafe(path):
    char_string = _unsafe_chars(path)
    if len(char_string) > 0:
        _LOGGER.warning('The unsafe characters %s detected in the filename "%s". '
                        'This may cause unexpected behaviour.',
                        char_string,
                        path)


class FileInfo():
    """
    Class files input into the BuildUp and the files in after building
    `path` is the path of the file relative to the root documentation directory. This
    must be relative and link to a file inside the root, BuildUp does not recognise
    files outside of root. Use `location_on_disk` to spoof the location of a file elsewhere.
    `dynamic_content` should be True for file that buildup can process, or any file
    that buildup generates.
    File a file that build up doesn't process the `location_on_disk` can be set,
    as default this is assumed to be the path. This is None if `dynamic_content` is True
    `content` is none if `dynamic_content` is False, else it is the contents of the buildup
    file.
    """

    def __init__(self,
                 path,
                 location_on_disk=None,
                 dynamic_content: bool = False,
                 content=None,
                 files_to_zip=None,
                 meta_info=None,
                 duplicate_of=None,
                 includes=None,
                 variables=None):

        self._path = as_posix(path)
        if posixpath.isabs(self._path):
            raise RuntimeError('FileInfo objects cannot specify paths outside the build'
                               f' directory. Requested path is "{self._path}"')

        self._dynamic_content = bool(dynamic_content)

        if isinstance(meta_info, dict):
            self._meta_info = meta_info
        elif meta_info is None:
            self._meta_info = {}
        else:
            raise TypeError('meta_info for a file should be a dictionary')

        if self._dynamic_content:
            self._variables = variables
            self._location_on_disk = None
            self._duplicate_of = duplicate_of
            if includes is None:
                self._includes = []
            else:
                self._includes = includes
            if content is not None:
                self._content = str(content)
                self._files_to_zip = None
            elif files_to_zip is not None:
                self._content = None
                self._files_to_zip = files_to_zip
            else:
                raise RuntimeError('Buildup file must have a content string')

        else:
            self._variables = None
            self._content = None
            self._files_to_zip = None
            self._duplicate_of = None
            self._includes = []
            # Use os.path here as it is the native location on this machine
            if location_on_disk is None:
                self._location_on_disk = os.path.normpath(self._path)
            else:
                self._location_on_disk = os.path.normpath(location_on_disk)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.as_dict())

    def __eq__(self, obj):
        if isinstance(obj, str):
            return self.path == as_posix(obj)
        if isinstance(obj, FileInfo):
            #This is a bit of a hack, should implement a file hash
            if self.path != obj.path:
                return False
            if self.dynamic_content != obj.dynamic_content:
                return False
            if self.location_on_disk != obj.location_on_disk:
                return False
            # if everything else matches return if the contents are equal
            return self.content == obj.content
        #equality not implemented for all other types
        return NotImplemented

    @property
    def dynamic_content(self):
        '''False if the output file is just a coppied file
        True if the content is dynamic_content by gitbuilding'''
        return self._dynamic_content

    @property
    def duplicate_of(self):
        '''
        If this page is a duplicate of another page due to multiple paths through
        the documentation, this will be the path to the original file. In not it is
        None
        '''
        return self._duplicate_of

    @property
    def includes(self):
        '''
        List of all pages this page includes content from
        '''
        return self._includes

    @property
    def variables(self):
        """
        Return any set variables for this file object
        """
        return self._variables

    @property
    def path(self):
        '''
        The output path of the file relative to the output directory or
        server root
        '''
        if self._path.startswith('..'):
            return 'orphaned_files/' + posixpath.basename(self._path)
        return self._path

    @property
    def location_on_disk(self):
        '''
        The current location of the file. This is None if the output
        content is dynamic_content.
        '''
        return self._location_on_disk

    @property
    def content(self):
        '''
        Returns the content of the file (this is only valid if `dynamic_content` is True)
        '''
        return self._content

    @property
    def files_to_zip(self):
        '''
        Return the list of files to be zipped if file_obj is for a dynamically created zipfile
        '''
        return self._files_to_zip

    @property
    def meta_info(self):
        '''
        Returns any meta information about the file
        '''
        return self._meta_info

    def as_dict(self):
        '''
        Serialise the file object as a dictionary
        '''
        output = {'path': self.path,
                  'dynamic_content': self._dynamic_content}
        if self.dynamic_content:
            output['content'] = self._content
        else:
            output['location_on_disk'] = self._location_on_disk
        return output
