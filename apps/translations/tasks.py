"""
Celery tasks for translation processing
"""
from celery import shared_task
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task
def translate_text_task(source_text, source_lang, target_lang):
    """
    Asynchronous translation task using AI models
    """
    try:
        # Import AI model utilities
        from apps.ai_models.utils import get_translation_model, translate_with_nllb
        
        # Get the translation model
        model, tokenizer = get_translation_model()
        
        # Perform translation
        translated_text = translate_with_nllb(
            model, tokenizer, source_text, source_lang, target_lang
        )
        
        return {
            'success': True,
            'translated_text': translated_text,
            'model_used': 'nllb-200'
        }
        
    except Exception as e:
        logger.error(f"Translation task failed: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task
def update_language_pair_stats():
    """
    Periodic task to update language pair statistics
    """
    from .models import LanguagePair
    
    try:
        for pair in LanguagePair.objects.all():
            pair.update_statistics()
        
        logger.info("Language pair statistics updated successfully")
        return {'success': True, 'message': 'Statistics updated'}
        
    except Exception as e:
        logger.error(f"Failed to update language pair stats: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task
def cleanup_old_cache():
    """
    Clean up old translation cache entries
    """
    from .models import TranslationCache
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        # Remove cache entries older than 30 days with low hit count
        cutoff_date = timezone.now() - timedelta(days=30)
        old_entries = TranslationCache.objects.filter(
            last_accessed__lt=cutoff_date,
            hit_count__lt=5
        )
        
        deleted_count = old_entries.count()
        old_entries.delete()
        
        logger.info(f"Cleaned up {deleted_count} old cache entries")
        return {'success': True, 'deleted_count': deleted_count}
        
    except Exception as e:
        logger.error(f"Cache cleanup failed: {str(e)}")
        return {'success': False, 'error': str(e)}