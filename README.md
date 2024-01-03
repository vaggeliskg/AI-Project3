ΚΑΛΑΜΠΟΚΗΣ ΕΥΑΓΓΕΛΟΣ 
1115202100045


ΠΑΡΑΔΕΙΓΜΑ ΕΚΤΕΛΕΣΗΣ: 

python codetry.py 11 fc

codetry.py:
    
Στο αρχείο αυτό βρίσκονται 4 συναρτήσεις που διαβάζουν από το αρχείο rlfap και δημιουργούν 1 λίστα με τις μεταβλητές, 1 dictionary με τα domains, 1 λίστα με τους περιορισμούς που χρησιμοποιείται από την constraints_check, και 1 dictionary με τους γείτονες κάθε μεταβλητής. Δίνεται σαν όρισμα από τον χρήστη
το instance και ο αλγόριθμος που θέλει να εκτελεστεί για τα οποία μετρείται ο χρόνος αλλά επειδή ο χρόνος διαφέρει ανάλογα με την υλοποίηση χρησιμοποιείται όπως και στις διαφάνειες σαν κριτήριο το πλήθος των κόμβων που έχουν επισκεφθεί και το πλήθος των ελέγχων συνέπειας

cpy.py:

Στην init του CSP αρχικοποιείται το dictionary με τα βάρη κάθε ακμής σε 1 μια μεταβλητή last_variable με το conflict_set της και ένα conflict set dictionary για όλες τις μεταβλητές που αρχικά είναι κενό. Το μόνο που έχει προστεθεί σε αυτό το αρχείο είναι η αύξηση των βαρών όταν προκύπτει domain wipeout στο forward checking και στο AC3b που χρησιμοποιεί ο mac και η domwdeg όπως αυτή αναγράφεται στο συνοδευτικό άρθρο της εκφώνησης.
Για την υλοποίηση του FC-CBJ χρειάστηκε βοήθεια από τις διαφάνειες και από ένα ακόμα άρθρο: https://www.dcs.bbk.ac.uk/~igor/papers/proceedings/ercimcbj.pdf. Καθένας από τους 4 αλγορίθμους επιστρέφει και το σύνολο των ελέγχων συνέπειας που έκανε


ΑΠΟΤΕΛΕΣΜΑΤΑ(στη συνοδευτική φωτογραφία): 

Όπου >500 το πρόγραμμα έτρεχε για πάνω απο 500 δευτερόλεπτα οπότε τερμάτιζε το thread που χρησιμοποιήσα
Όπου υπάρχει not solved σημαίνει ότι το result που επέστρεφε το πρόγραμμα δεν ήταν dictionary αλλά None

Όπως φαίνεται και στη θεωρία για το πλήθος των κόμβων ισχύει: FC-CBJ <= FC και MAC <= FC 

Και για το πλήθος των ελέγχων συνέπειας ισχύει: FC-CBJ <= FC

Η min conflicts δεν είναι τόσο αποδοτική αφού στο δικό μου μηχάνημα τουλάχιστον δεν κατάφερε να λύσει κάποιο instance σε < 500 δευτερόλεπτα

