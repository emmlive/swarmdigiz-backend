# -*- coding: utf-8 -*-

"""
SwarmDigiz Campaign Launch Engine

Handles launching campaigns to marketing platforms.
(Current version simulates launch safely)
"""

from connectors.facebook_ads_connector import FacebookAdsConnector
from connectors.google_ads_connector import GoogleAdsConnector


def launch_google_campaign(assets):

    connector = GoogleAdsConnector()

    payload = {
        "headline": assets["google_ad"]["headline"],
        "description": assets["google_ad"]["description"],
        "cta": assets["google_ad"]["cta"],
    }

    response = connector.execute(payload)

    return response


def launch_facebook_campaign(assets):

    connector = FacebookAdsConnector()

    payload = {
        "headline": assets["facebook_ad"]["headline"],
        "text": assets["facebook_ad"]["text"],
        "cta": assets["facebook_ad"]["cta"],
    }

    response = connector.execute(payload)

    return response


def launch_full_campaign(assets):

    google = launch_google_campaign(assets)
    facebook = launch_facebook_campaign(assets)

    return {
        "google": google,
        "facebook": facebook,
    }