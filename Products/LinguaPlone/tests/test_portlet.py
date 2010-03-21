from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.browser.language import Renderer
from Products.LinguaPlone.tests import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class TestLanguagePortlet(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')
        self.german.setLanguage('de')

    def testRenderPortlet(self):
        request = self.app.REQUEST
        renderer = Renderer(self.english, request, None, None, None)
        output = renderer.render()
        self.assert_('<dl class="portlet portletLanguage">' in output)
        de_path = self.german.absolute_url()
        de_link = '<a href="%s?set_language=de" title="German">' % de_path
        self.assert_(de_link in output)
        en_path = self.english.absolute_url()
        en_link = '<a href="%s?set_language=en" title="English">' % en_path
        self.assert_(en_link in output)

    def testRenderPortletOnUntranslatableContent(self):
        request = self.app.REQUEST
        renderer = Renderer(self.portal, request, None, None, None)
        output = renderer.render()
        path = self.portal.absolute_url()
        de_link = '<a href="%s?set_language=de" title="German">' % path
        self.assert_(de_link in output)
        en_link = '<a href="%s?set_language=en" title="English">' % path
        self.assert_(en_link in output)

    def testRenderPortletWithFlags(self):
        request = self.app.REQUEST
        ltool = getToolByName(self.portal, 'portal_languages')
        ltool.display_flags = True
        renderer = Renderer(self.english, request, None, None, None)
        output = renderer.render()
        self.assert_('de.gif' in output)
        self.assert_('gb.gif' in output)

    def testRenderPortletWithoutCookieNegotiation(self):
        request = self.app.REQUEST
        ltool = getToolByName(self.portal, 'portal_languages')
        ltool.use_cookie_negotiation = False
        renderer = Renderer(self.english, request, None, None, None)
        output = renderer.render()
        self.assertEquals(output.strip(), u'')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLanguagePortlet))
    return suite