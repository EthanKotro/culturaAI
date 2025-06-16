"""
AI Model utilities and helper functions
"""
import hashlib
import time
import logging
from django.conf import settings
from django.core.cache import cache
from .models import AIModel, ModelRequest, ModelCache

logger = logging.getLogger(__name__)


def get_translation_model():
    """Get the active translation model"""
    try:
        model_config = AIModel.objects.get(
            model_type='translation',
            is_active=True,
            is_default=True
        )
        
        # In a real implementation, this would load the actual model
        # For now, we'll return a mock model configuration
        return {
            'name': model_config.name,
            'path': model_config.model_path,
            'config': model_config
        }
        
    except AIModel.DoesNotExist:
        logger.error("No active translation model found")
        return None


def translate_with_nllb(model_config, source_text, source_lang, target_lang):
    """
    Translate text using NLLB model
    This is a placeholder implementation
    """
    start_time = time.time()
    
    try:
        # Create input hash for caching
        input_hash = hashlib.sha256(
            f"{source_text}_{source_lang}_{target_lang}".encode()
        ).hexdigest()
        
        # Check cache first
        try:
            cached_result = ModelCache.objects.get(
                model=model_config['config'],
                input_hash=input_hash
            )
            
            if not cached_result.is_expired():
                cached_result.hit_count += 1
                cached_result.save()
                
                processing_time = time.time() - start_time
                
                # Log request
                ModelRequest.objects.create(
                    model=model_config['config'],
                    input_text=source_text,
                    output_text=cached_result.output_text,
                    source_language=source_lang,
                    target_language=target_lang,
                    processing_time=processing_time,
                    success=True
                )
                
                return cached_result.output_text
                
        except ModelCache.DoesNotExist:
            pass
        
        # Perform actual translation (mock implementation)
        # In production, this would use the actual NLLB model
        language_map = {
            'en': 'English',
            'ki': 'Kikuyu',
            'luo': 'Luo',
            'kam': 'Kamba'
        }
        
        target_lang_name = language_map.get(target_lang, target_lang)
        translated_text = f"[{target_lang_name} Translation] {source_text}"
        
        processing_time = time.time() - start_time
        
        # Cache the result
        ModelCache.objects.create(
            model=model_config['config'],
            input_hash=input_hash,
            input_text=source_text,
            output_text=translated_text
        )
        
        # Log request
        ModelRequest.objects.create(
            model=model_config['config'],
            input_text=source_text,
            output_text=translated_text,
            source_language=source_lang,
            target_language=target_lang,
            processing_time=processing_time,
            success=True
        )
        
        # Update model metrics
        model_config['config'].update_metrics(processing_time, success=True)
        
        return translated_text
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Translation failed: {str(e)}")
        
        # Log failed request
        ModelRequest.objects.create(
            model=model_config['config'],
            input_text=source_text,
            source_language=source_lang,
            target_language=target_lang,
            processing_time=processing_time,
            success=False,
            error_message=str(e)
        )
        
        # Update model metrics
        model_config['config'].update_metrics(processing_time, success=False)
        
        raise e


def get_tts_model(language_code):
    """Get TTS model for specific language"""
    try:
        from .models import LanguageModel
        lang_model = LanguageModel.objects.get(
            language_code=language_code,
            is_supported=True
        )
        
        if lang_model.tts_model and lang_model.tts_model.is_active:
            return {
                'name': lang_model.tts_model.name,
                'path': lang_model.tts_model.model_path,
                'config': lang_model.tts_model
            }
        
    except LanguageModel.DoesNotExist:
        pass
    
    # Fallback to default TTS model
    try:
        default_tts = AIModel.objects.get(
            model_type='tts',
            is_active=True,
            is_default=True
        )
        
        return {
            'name': default_tts.name,
            'path': default_tts.model_path,
            'config': default_tts
        }
        
    except AIModel.DoesNotExist:
        logger.error("No TTS model found")
        return None


def generate_speech(text, language_code, voice_settings=None):
    """
    Generate speech from text using TTS model
    This is a placeholder implementation
    """
    start_time = time.time()
    
    try:
        tts_model = get_tts_model(language_code)
        if not tts_model:
            raise Exception("No TTS model available")
        
        # Create input hash for caching
        settings_str = str(voice_settings) if voice_settings else ""
        input_hash = hashlib.sha256(
            f"{text}_{language_code}_{settings_str}".encode()
        ).hexdigest()
        
        # Check cache
        try:
            cached_result = ModelCache.objects.get(
                model=tts_model['config'],
                input_hash=input_hash
            )
            
            if not cached_result.is_expired():
                cached_result.hit_count += 1
                cached_result.save()
                
                processing_time = time.time() - start_time
                
                # Log request
                ModelRequest.objects.create(
                    model=tts_model['config'],
                    input_text=text,
                    output_text=f"Audio file: {cached_result.output_text}",
                    source_language=language_code,
                    processing_time=processing_time,
                    success=True
                )
                
                return cached_result.output_text  # This would be audio file path
                
        except ModelCache.DoesNotExist:
            pass
        
        # Generate speech (mock implementation)
        # In production, this would use actual TTS model
        audio_filename = f"tts_{input_hash[:8]}.wav"
        audio_path = f"/media/audio/{audio_filename}"
        
        processing_time = time.time() - start_time
        
        # Cache the result
        ModelCache.objects.create(
            model=tts_model['config'],
            input_hash=input_hash,
            input_text=text,
            output_text=audio_path
        )
        
        # Log request
        ModelRequest.objects.create(
            model=tts_model['config'],
            input_text=text,
            output_text=f"Audio file: {audio_path}",
            source_language=language_code,
            processing_time=processing_time,
            success=True
        )
        
        # Update model metrics
        tts_model['config'].update_metrics(processing_time, success=True)
        
        return audio_path
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"TTS generation failed: {str(e)}")
        
        # Log failed request
        if 'tts_model' in locals() and tts_model:
            ModelRequest.objects.create(
                model=tts_model['config'],
                input_text=text,
                source_language=language_code,
                processing_time=processing_time,
                success=False,
                error_message=str(e)
            )
            
            tts_model['config'].update_metrics(processing_time, success=False)
        
        raise e


def cleanup_expired_cache():
    """Clean up expired cache entries"""
    from django.utils import timezone
    
    expired_entries = ModelCache.objects.filter(
        expires_at__lt=timezone.now()
    )
    
    count = expired_entries.count()
    expired_entries.delete()
    
    logger.info(f"Cleaned up {count} expired cache entries")
    return count