from copy import deepcopy

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.utilities.marker import mark

from plone.dexterity.utils import createContentInContainer

from .interfaces import IFourOhFourPage


class FourOhFourView(BrowserView):

    def render(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')

        results = catalog.searchResults(
            object_provides=IFourOhFourPage.__identifier__
        )

        if not len(results):
            return

        obj = results[0].getObject()
        return obj()


class ControlPanel(BrowserView):

    # XXX: Use the IFourOhFourPage marker interface instead
    # of hardcoded URL

    def get404url(self, language):
        context = self.context
        languages_tool = getToolByName(context, 'portal_languages')
        default_language = languages_tool.getDefaultLanguage()

        url_tool = getToolByName(context, 'portal_url')
        site_url = url_tool()

        if language == default_language:
            return site_url + '/fourohfour'

        return site_url + '/' + language + '/fourohfour'

    def exists404(self, language):
        context = self.context
        languages_tool = getToolByName(context, 'portal_languages')
        default_language = languages_tool.getDefaultLanguage()

        url_tool = getToolByName(context, 'portal_url')
        folder = url_tool.getPortalObject()

        if language != default_language:
            try:
                folder = folder.restrictedTraverse(language)
            except KeyError:
                return False

        return hasattr(folder.aq_base, 'fourohfour')

    def language_folder_exists(self, language):
        context = self.context
        languages_tool = getToolByName(context, 'portal_languages')
        default_language = languages_tool.getDefaultLanguage()

        if language == default_language:
            return True

        url_tool = getToolByName(context, 'portal_url')
        folder = url_tool.getPortalObject()

        return hasattr(folder, language)

    @property
    def languages(self):
        results = []
        context = self.context
        languages_tool = getToolByName(context, 'portal_languages')

        available_languages = languages_tool.getAvailableLanguages()
        supported_languages = languages_tool.getSupportedLanguages()

        for language in supported_languages:
            new_dict = deepcopy(
                available_languages.get(language, {})
            )

            new_dict['id'] = language
            new_dict['url'] = self.get404url(language)
            new_dict['parent_exists'] = self.language_folder_exists(language)
            new_dict['exists'] = self.exists404(language)

            results.append(new_dict)

        return results


class CreateFourOhFourPage(BrowserView):

    def __call__(self):
        context = self.context

        languages_tool = getToolByName(context, 'portal_languages')
        default_language = languages_tool.getDefaultLanguage()

        request = self.request
        language = request.get('language', default_language)

        url_tool = getToolByName(context, 'portal_url')
        folder = url_tool.getPortalObject()

        if language != default_language:
            folder = folder.restrictedTraverse(language)

        if not hasattr(folder, 'fourohfour'):
            folder = folder.aq_base

            item = createContentInContainer(
                folder, 'Document', checkConstraints=True,
                title='404 page'
            )

            # Since the document type provides the INameFromTitle
            # behavior, we cannot override it, so we need to
            # rename the object :(

            folder.manage_renameObject(item.id, 'fourohfour')

            # Mark the element using the marker interface
            mark(item, IFourOhFourPage)

            # Remember to reindex, marking an object does _not_
            # trigger events.
            item.reindexObject()

        return request.RESPONSE.redirect(
            folder.absolute_url() + '/fourohfour/edit'
        )
