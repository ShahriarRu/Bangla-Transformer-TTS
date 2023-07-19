from phonemizer import phonemize
from phonemizer.separator import Separator

text = "আমাকে মাত্র দশ হাজার বার ট্রেইন করা হয়েছে"

phn = phonemize(
    text,
    language='bn',
    backend='espeak',
    separator=Separator(phone=None, word=' ', syllable='|'),
    strip=True,
    preserve_punctuation=True,
    njobs=4)
print(phn)
