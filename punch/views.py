from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import StudySession, Break
from collections import defaultdict

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StudySession
import random

@login_required
def dashboard(request):
    latest_session = StudySession.objects.filter(user=request.user).order_by('-start_time').first()

    # Determine which GIF to show
    session_gif = 'images/dog.jpg'  # default
    if latest_session:
        if latest_session.end_time is None:  # ongoing study session
            # Check if currently on break
            current_break = latest_session.breaks.filter(break_end__isnull=True).first()
            if current_break:
                session_gif = 'images/shinchan_break.gif'
            else:
                session_gif = 'images/study.gif'
    quotes = [
    "I’m not lazy… I’m on energy-saving mode. ⚡😴",
    "Life is short. Smile while you still have teeth. 😁🦷",
    "Procrastinate today… panic tomorrow. ⏳😅",
    "Coffee first, adulting second. ☕💼",
    "I followed my heart and it led me to the fridge. ❤️🧊🍕",
    "Some call it chaos, we call it creativity. 🎨😎",
    "Brains are awesome… I wish everyone had one! 🧠😂",
    "Error 404: Motivation not found… but coffee helps. ☕💻",
    "I’m on a seafood diet. I see food, and I eat it. 🐟🍔",
    "Keep calm and pretend it’s on the syllabus. 📚😏",
    "I need six months of vacation… twice a year. 🏖️😴",
    "Life is too short to remove USB safely. 🔌💥",
    "Organized people are just too lazy to look for stuff. 📂🙃",
    "I’m multitasking: I can listen, ignore and forget at the same time. 👂🤷‍♂️🌀",
    "Smile… it confuses people. 😏😜",
    "My life is a constant battle between my love for food and not wanting to get fat. 🍕⚔️🏋️",
    "I’m not weird, I’m limited edition. 🌟🦄",
    "Some days I amaze myself. Other days… I look for my phone while holding it. 📱🤦‍♂️",
    "If life gives you lemons, add vodka and throw a party. 🍋🍸🎉",
    "Keep shining… even if your WiFi is weak. 🌟📶",
    "Sleep like no one is watching. 😴🛌",
    "I don’t need a motivational quote… I need coffee. ☕😎",
    "Why fall in love when you can fall into pizza? 🍕❤️",
    "Life happens… coffee helps. ☕💫",
    "I’m silently correcting your grammar. 🤫✍️",
    "Running late is my cardio. 🏃‍♂️⌚",
    "I speak fluent sarcasm. 😏🗣️",
    "Mondays are proof that time machines exist. ⏰😩",
    "Reality called… I hung up. 📞🙅‍♂️",
    "I put the ‘pro’ in procrastinate. 🏆😅",
    "Brains are awesome… I prefer chocolate. 🍫🧠",
    "Don’t follow your dreams… chase snacks. 🍩🏃‍♀️",
    "I’m on a 24-hour nap cycle. 🛌🕒",
    "Work hard so your cat can live better. 🐱💼",
    "Life is short… smile while your phone battery lasts. 📱😁",
    "I don’t sweat… I sparkle. ✨💦",
    "Calories don’t count on weekends. 🍰🕺",
    "I plan, God laughs. 😂📅",
    "I’m not arguing, I’m explaining why I’m right. 😎💬",
    "Life is better when you laugh… or nap. 😆😴",
    "I don’t get older, I level up. 🎮😎",
    "Exercise? I thought you said extra fries! 🍟😂",
    "Don’t worry… be happy… and eat pizza. 🍕😋",
    "Life without coffee is scary. ☕😱",
    "Nap hard, play harder. 😴🎉",
    "Chocolate solves everything. 🍫✨",
    "My brain has too many tabs open. 🧠💻",
    "If at first you don’t succeed… skydiving is not for you. 🪂😅",
    "I’m not clumsy… the floor just hates me. 🙃💥",
    "Sarcasm is my superpower. 😏🦸",
    "I’m not ignoring you… I’m just on silent mode. 🤫📴",
    "I need six months of sleep… twice a year. 🛌😴",
    "My life is a romantic comedy… minus the romance. 🎬😂",
    "I put the ‘fun’ in dysfunctional. 🤪🎉",
    "I’m late… but I’m fabulous. 💃⌚",
    "Some call it procrastination… I call it creative thinking. 🤔💡",
    "WiFi and coffee… my two lifelines. 📶☕",
    "I’m on a diet… I see food, I eat it. 🍲😋",
    "I’m not lazy… I’m just on power-saving mode. ⚡😌",
    "Life is too short to fold fitted sheets. 🛏️😂",
    "I can’t adult today… tomorrow doesn’t look good either. 😅📅",
    "I dance like nobody’s watching… because they’re not. 💃😂",
    "Some mistakes are too fabulous to repeat. 💅😎",
    "I’m not crazy… my reality is just different. 😜🌈",
    "Nap first, conquer later. 😴🏆",
    "I’m not short… I’m concentrated awesome. 😎✨",
    "Life is like a selfie… focus on the good angles. 🤳😊",
    "I’m allergic to mornings. 🌞😩",
    "Running late counts as exercise. 🏃‍♀️⌚",
    "I’m not bossy… I just have better ideas. 😏💡",
    "I whisper to my WiFi… stay strong. 📶🙏",
    "I’m on a seafood diet… I see food, I eat it. 🐟😂",
    "My bed is a magical place… I suddenly remember everything I forgot to do. 🛌✨",
    "If you can’t convince them… confuse them. 😏🌀",
    "I like long romantic walks… to the fridge. 🚶‍♂️🍕",
    "I’m multitasking: eating and procrastinating at the same time. 🍔📚",
    "Chocolate doesn’t ask questions… chocolate understands. 🍫❤️",
    "Life is short… smile while you still have WiFi. 😁📶",
    "Some days I amaze myself… other days, I’m amazed I exist. 🤯😂",
    "I’m not late… I’m on my own time zone. ⏰😎",
    "Exercise? I thought you said extra dessert! 🍰😂",
    "I pretend to work… my keyboard knows the truth. ⌨️😅",
    "I’m not addicted to coffee… we’re in a committed relationship. ☕❤️",
    "Brains are awesome… I wish everyone had one. 🧠😏",
    "Nap hard… play harder. 😴🎉",
    "I don’t trip… I do random gravity checks. 😎💥",
    "I’m silently judging your life choices. 🤨😂",
    "I smile… because I have no idea what’s going on. 😏😅",
    "Life is a soup… I’m a fork. 🍲😂",
    "I’m not lazy… I’m just in energy-saving mode. ⚡😌",
    "I don’t rise and shine… I caffeinate and hope. ☕✨",
    "If life gives you lemons… squirt someone in the eye. 🍋😜",
    "I’m awesome… but humble enough to admit it. 😎✌️",
    "I plan… then life laughs at me. 😂📅",
    "I have a black belt in keeping it real. 🥋😎",
    "I’m on a mission to avoid adulthood… it’s going well. 🛌💼",
    "Why chase dreams… when you can chase snacks? 🍩🏃‍♂️",
    "Life is short… eat the dessert first. 🍰😋",
    "I’m multitasking… I can ignore you and think about snacks simultaneously. 🤔🍫",
    "I put the ‘fun’ in dysfunctional. 🤪🎉",
    "I live in my own little world… it’s fine, they know me here. 🌎😏",
    "I’m not late… everyone else is just early. ⏰😎",
    "Life’s too short… take a nap. 😴✨",
    "I’m not shy… I just don’t talk to stupid people. 😏🙄",
    "I’m not arguing… I’m just explaining why I’m right. 😎💬",
    "I’m limited edition… handle with care. 🌟🦄",
    "I follow my heart… it usually leads me to snacks. ❤️🍕",
    "Nap now… conquer later. 😴🏆",
    "I sparkle… even on Monday mornings. ✨😎"
]

    quote = random.choice(quotes)

    # 🏆 Find the longest (record) study session
    longest_session = None
    highest_duration = 0  # in minutes

    all_sessions = StudySession.objects.filter(user=request.user, end_time__isnull=False)
    for s in all_sessions:
        duration = (s.end_time - s.start_time).total_seconds() / 60
        if duration > highest_duration:
            highest_duration = duration
            longest_session = s

    # Format record time
    if highest_duration > 0:
        hours = int(highest_duration // 60)
        minutes = int(highest_duration % 60)
        highest_study_time = f"{hours}h {minutes}m"
    else:
        highest_study_time = None

    # Send everything to template
    context = {
        'latest_session': latest_session,
        'quote': quote,
        'session_gif': session_gif,
        'highest_study_time': highest_study_time,
    }

    return render(request, 'punch/dashboard.html', context)


@login_required
def start_study(request):
    # End any unfinished session before starting a new one
    unfinished = StudySession.objects.filter(user=request.user, end_time__isnull=True).first()
    if unfinished:
        messages.warning(request, "You already have a session running!")
        return redirect('dashboard')

    StudySession.objects.create(user=request.user, start_time=timezone.now())
    messages.success(request, "🎯 You started studying! Stay focused!")
    return redirect('dashboard')


@login_required
def end_study(request):
    session = StudySession.objects.filter(user=request.user, end_time__isnull=True).order_by('-start_time').first()
    if not session:
        messages.warning(request, "No active session found to end.")
        return redirect('dashboard')

    session.end_time = timezone.now()
    session.total_minutes = int((session.end_time - session.start_time).total_seconds() / 60)
    session.save()

    messages.success(request, f"✅ Session ended! Total study time: {session.total_minutes // 60}h {session.total_minutes % 60}m")
    return redirect('dashboard')


@login_required
def start_break(request):
    session = StudySession.objects.filter(user=request.user, end_time__isnull=True).order_by('-start_time').first()
    if not session:
        messages.warning(request, "Start a session before taking a break.")
        return redirect('dashboard')

    ongoing_break = Break.objects.filter(session=session, break_end__isnull=True).first()
    if ongoing_break:
        messages.warning(request, "You're already on a break!")
        return redirect('dashboard')

    Break.objects.create(session=session, break_start=timezone.now())
    messages.info(request, "☕ Break started! Rest your mind.")
    return redirect('dashboard')


@login_required
def end_break(request):
    brk = Break.objects.filter(session__user=request.user, break_end__isnull=True).order_by('-break_start').first()
    if not brk:
        messages.warning(request, "No active break found to end.")
        return redirect('dashboard')

    brk.break_end = timezone.now()
    brk.break_minutes = int((brk.break_end - brk.break_start).total_seconds() / 60)
    brk.save()

    messages.success(request, f"🚀 Break ended! Duration: {brk.break_minutes} mins.")
    return redirect('dashboard')

@login_required
def session_list(request):
    # Filter only the logged-in user's sessions
    sessions = StudySession.objects.filter(user=request.user).order_by('-start_time')

    grouped_sessions = defaultdict(list)

    for s in sessions:
        # Convert UTC → local time for correct day grouping
        local_start_time = timezone.localtime(s.start_time)
        date_str = local_start_time.strftime('%d %B %Y')

        total_break_minutes = sum(b.break_minutes for b in s.breaks.all())
        s.total_hours = s.total_minutes // 60
        s.total_mins_only = s.total_minutes % 60

        s.productive_minutes = max(s.total_minutes - total_break_minutes, 0)
        s.productive_hours = s.productive_minutes // 60
        s.productive_mins_only = s.productive_minutes % 60

        grouped_sessions[date_str].append(s)

    grouped_list = list(grouped_sessions.items())  

    return render(request, 'punch/sessions.html', {'grouped_sessions': grouped_list})

